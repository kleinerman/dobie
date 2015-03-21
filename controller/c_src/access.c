#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <sys/epoll.h>
#include <pthread.h>
#include <mqueue.h>
#include <access.h>


/*
 * Returns the number of occurrences of the string str found in
 * the program arguments.
 */
int get_number_of(int argc, char** argv, const char *str) {
    int i;
    int count = 0;

    for (i=1; i<argc; i++) {
        if ( strcmp(argv[i], str) == 0 )
            count++;
    }

    return count;
}


/*
 * Parses the command-line arguments (GPIO pins) and fill the door structures
 * A negative attribute means that it is not in use
 */
int parser(int argc, char **argv, door_t *door) {
    int i, j, number_of_doors;

    // the arguments should start with door ID
    if ( strcmp(argv[1], "--door") != 0 ) {
        printf("Error: You should declare a door ID before declaring GPIO pins\n");
        return -1;
    }

    // number of door in this controller
    number_of_doors = get_number_of(argc, argv, "--door");

    // initialization: a negative value means not in use.
    for (i = 0; i < number_of_doors; i++) {
        door[i].id = -1;
        door[i].i0 = -1;
        door[i].i1 = -1;
        door[i].o0 = -1;
        door[i].o1 = -1;
        door[i].button = -1;
        door[i].state = -1;
    }

    // parses the arguments and fills the door structures
    j = -1;
    for (i=1; i<argc; i=i+2) { // argument(i) value(i+1) argument(i+2)
         if ( strcmp(argv[i], "--door") == 0 ) {
             j++; // increase the index for each door
             door[j].id = atoi(argv[i+1]);
         }
         if ( strcmp(argv[i], "--i0") == 0 )
             door[j].i0 = atoi(argv[i+1]);
         if ( strcmp(argv[i], "--i1") == 0 )
             door[j].i1 = atoi(argv[i+1]);
         if ( strcmp(argv[i], "--o0") == 0 )
             door[j].o0 = atoi(argv[i+1]);
         if ( strcmp(argv[i], "--o1") == 0 )
             door[j].o1 = atoi(argv[i+1]);
         if ( strcmp(argv[i], "--button1") == 0 )
             door[j].button = atoi(argv[i+1]);
         if ( strcmp(argv[i], "--state") == 0 )
             door[j].state = atoi(argv[i+1]);
    }

    return 0;
}


/*
 * Export the GPIO to userspace. On success it returns 0, else returns -1
 * In a near future, this function will be implemented in Python
 */
int export_gpio(unsigned int gpio) {
    int fd, len;
    char str_gpio[10];
    
    if ((fd = open("/sys/class/gpio/export", O_WRONLY )) < 0 ) {
        fprintf(stderr,"Error(%d) opening /sys/class/gpio/export: %s\n", errno, strerror(errno));
        return -1;
    }

    // get the length of the gpio string
    len = sprintf(str_gpio, "%d", gpio);

    if ( write(fd, str_gpio, len) == 0) {
        fprintf(stderr,"Error(%d) writing /sys/class/gpio/export: %s\n", errno, strerror(errno));
        return -1;
    }

    close(fd);
    return 0; // success GPIO export

}


/*
 * Set the gpio direction: IN(1) or OUT(0)
 * It returns 0 on success
 * ++ In a near future, this function will be implemented in Python ++
 */
int gpio_set_direction(unsigned int gpio, unsigned int direction) {
    int fd;
    char filename[40];
    char *str_direction[2] = { "out" , "in" };
    
    snprintf(filename, sizeof(filename), "/sys/class/gpio/gpio%d/direction", gpio);
    
    if ((fd = open(filename, O_WRONLY)) < 0) {
        fprintf(stderr,"Error(%d) opening %s: %s\n", errno, filename, strerror(errno));
        return -1;
    }

    if ( write(fd, str_direction[direction], strlen(str_direction[direction])) == 0 ) {
        fprintf(stderr,"Error(%d) writing %s: %s\n", errno, filename, strerror(errno));
        return -1;
    }

    close(fd);
    return 0;
}


/* Select the signal edge that will make poll-on the "value" file return.
 * It returns 0 on success
 * ++ In a near future, this function will be implemented in Python ++
 */
int gpio_set_edge(unsigned int gpio, unsigned int edge) {
    int fd;
    char filename[40];
    char *str_edge[4] = {"none", "falling", "rising", "both"};

    snprintf(filename, sizeof(filename), "/sys/class/gpio/gpio%d/edge", gpio);

    if ((fd = open(filename, O_WRONLY)) < 0) {
        fprintf(stderr,"Error(%d) opening %s: %s\n", errno, filename, strerror(errno));
        return -1;
    }

    if ( write(fd, str_edge[edge], strlen(str_edge[edge])) == 0 ) {
        fprintf(stderr,"Error(%d) writing %s: %s\n", errno, filename, strerror(errno));
    }

    close(fd);
    return 0;
}


/*
 * This function is usead in a thread. It is resposible to write 0 in a register if it is listening
 * the line D0, or write 1 if it is listening D1. There are two thread per card reader: one for D0
 * and other for D1. Together will count 26bits acording to the wiegand protocol. The thread that
 * fill the register with the last incoming bit (number 26) is responsible to form the card number
 * and restart the register.
 */
void* read_card (void *args) {
    char filename[40];
    char str_card_number[8];
    char message[50];
    int i; // index for for cicle
    int fd[2]; // file descriptors
    int epfd; // epool file descriptor
    int card_number;
    int mask;
    struct epoll_event ev[2];
    struct epoll_event events[2];
    struct read_card_args *arg = (struct read_card_args*) args; //arguments passed to the thread
    int gpio[] = {arg->d0, arg->d1};

    // GPIOs initialization
    // export the gpio to the filesystem
    if ( export_gpio(arg->d0) == -1 ) exit(1);
    if ( export_gpio(arg->d1) == -1 ) exit(1);
    // set the gpio as an input
    if ( gpio_set_direction(arg->d0, IN) == -1 ) exit(1);
    if ( gpio_set_direction(arg->d1, IN) == -1 ) exit(1);
    // set the edge to wait for
    if ( gpio_set_edge(arg->d0, FALLING) == -1 ) exit(1);
    if ( gpio_set_edge(arg->d1, FALLING) == -1 ) exit(1);

    // create a new epool instance
    epfd = epoll_create(1);
    if (epfd == -1) {
        fprintf(stderr,"Error(%d) creating the epoll: %s\n", errno, strerror(errno));
        exit(1);
    }

    for (i=0; i<2; i++) {
        sprintf(filename, "/sys/class/gpio/gpio%d/value", gpio[i]);
        fd[i] = open(filename, O_RDWR | O_NONBLOCK);
        if (fd[i] == -1) {
            fprintf(stderr,"Error(%d) opening %s: %s\n", errno, filename, strerror(errno));
            exit(1);
        }
        ev[i].events = EPOLLIN | EPOLLET | EPOLLPRI;
        ev[i].data.fd = fd[i];
        // Add the file descriptors to the interest list for epfd
        epoll_ctl(epfd, EPOLL_CTL_ADD, fd[i], &ev[i]);
    }

    epoll_wait(epfd, events, 2, -1);  // first time it triggers with current state, so ignore it

    while (1) {
        mask = 33554432; // mask initialitation: 00000010000000000000000000000000
        card_number = 0; // initialize the card number

        while (mask != 0) {
            epoll_wait(epfd, events, 2, -1); // wait for an evente. Only fetch up one event
            if (events[0].data.fd == fd[1]) { // if the event was a D1, add 1 to the card number buffer and shift the mask
                card_number = card_number | mask;
            }
            mask = mask >> 1; // if the event was D0, only shift the mask 
        }

        /* If the mask is 0, the mask has been shifted 26 time, therefore the card has been read.
         * It is time to generate the card number, put this number in the OS queue, wait a short
         * time and clean the mask and the card number buffer. 
         */

        // deregister the target file descriptors from the epoll instance referred by epfd. Events are ignored
        for (i=0;i<2;i++)  {
            epoll_ctl(epfd, EPOLL_CTL_DEL, fd[i], &ev[i]);
        }

        /* generate the card number
         * card number = (xxxxxxxxxxxxxxxxxxxxxxxxxx AND 01111111111111111111111110) one left shift
         */
        card_number = (card_number & 33554430) >> 1;
        
        // preparing the queue message for sending
        sprintf(message, "%d;%c;card=%08d", arg->door_id, arg->side, card_number);

        // put the message into the queue
        mq_send(arg->mq, message, strlen(message), 1); // the '\0' caracter is not sent in the queue
        
        //just for testing propuse
        printf("%s\n", message);

        /* most devices transmit and recieve pulses around 50uS wide and with a gap of 5000uS between
         * pulses, so wait at least 26 times 5050uS (5000uS pulse gap + 50us pulse ) to avoid out of 
         * phase pulses
         */
        usleep(132000);

        // register again the file descriptors in the epoll epfd
        for (i=0; i<2; +i++) 
            epoll_ctl(epfd, EPOLL_CTL_ADD, fd[i], &ev[i]);

        epoll_wait(epfd, events, 2, -1);  // first time it triggers with current state, so ignore it
    }

    // this part of the code should never be executed
    close(epfd);
    for (i=0; i<2; i++) 
        close(fd[i]);
    return NULL;
}


/*
 * This function starts one thread per reader.
 * Each thread reads the card reader lines (D0 and D1), form the card number and
 * sends to the queue a message with the card number.
 */
int start_readers(int number_of_doors, int number_of_readers, door_t *door, pthread_t *thread, mqd_t mq) {
    int i; // array index
    struct read_card_args *args; // thread arguments

    args = (struct read_card_args *)malloc(sizeof(struct read_card_args) * number_of_readers);

    for (i=0 ; i<number_of_doors; i++) {
        if (door[i].i0 != -1 && door[i].i1 != -1 ) { // if the door has input card reader
            args->door_id = door[i].id;
            args->d0 = door[i].i0;
            args->d1 = door[i].i1;
            args->side = 'i';
            args->mq = mq;

            pthread_create(thread, NULL, read_card, (void *)args);
            thread++;
            args++;
        }
        if (door[i].o0 != -1 && door[i].o1 != -1 ) { // if the door has output card reader
            args->door_id = door[i].id;
            args->d0 = door[i].o0;
            args->d1 = door[i].o1;
            args->side = 'o';
            args->mq = mq;

            pthread_create(thread, NULL, read_card, (void *)args);

            thread++;
            args++;
        }

    }

    return 0;
}


int buttons (int number_of_doors, door_t *door, pthread_t *thread, mqd_t mq) {
    char filename[40];
    int **bttn_tbl;
    int i;
    int j=0;
    int epfd; // epool file descriptor
    struct epoll_event *ev;
    struct epoll_event *events;

    ev = (struct epoll_event *)malloc(sizeof(struct epoll_event) * number_of_buttons);
    events = (struct epoll_event *)malloc(sizeof(struct epoll_event) * number_of_buttons);

    /* Allocate memory for a table. The table has 2 columns and many rows as the number of buttons.
     * The 2 columns: the door_ID and file descriptor of the button.
     */
    bttn_tbl = (int **) malloc(sizeof(int *) * number_of_buttons);
    for (i=0; i<number_of_buttons; i++)
        bttn_tbl[i] = (int *) malloc(sizeof(int) * 2);

    //
    for (i=0; i<number_of_doors; i++) {
        if (door[i].button != -1) {     // if the door has button

            bttn_tbl[j][0] = door[i].id; // save the door id in the first col of the table

            // export the gpio to the filesystem
            if (export_gpio(door[i].button) == -1) exit(1);
            // set the gpio as an input
            if (gpio_set_direction(door[i].button, IN) == -1 ) exit(1);
            // set the edge to wait for
            if ( gpio_set_edge(door[i].button, FALLING) == -1 ) exit(1);

            // save the button fd in the second col of the table
            sprintf(filename, "/sys/class/gpio/gpio%d/value", door[i].button);
            bttn_tbl[j][1] = open(filename, O_RDWR | O_NONBLOCK);
            if (bttn_tbl[j][1] == -1) {
                fprintf(stderr,"Error(%d) opening %s: %s\n", errno, filename, strerror(errno));
                exit(1);
            }

            ev[j].events = EPOLLIN | EPOLLET | EPOLLPRI;
            ev[j].data.fd = bttn_tbl[j][1];
            // Add the file descriptors to the interest list for epfd
            epoll_ctl(epfd, EPOLL_CTL_ADD, bttn_tbl[j][1], &ev[j]); 

        }

        // create a new epool instance
        epfd = epoll_create(1);
        if (epfd == -1) {
            fprintf(stderr,"Error(%d) creating the epoll: %s\n", errno, strerror(errno));
            exit(1);
        }

        epoll_wait(epfd, events, number_of_buttons, -1);  // first time it triggers with current state, so ignore it





    return 0;
}

