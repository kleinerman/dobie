#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <sys/epoll.h>
#include <pthread.h>
#include <mqueue.h>
#include <unistd.h>
#include <libioiface.h>
#include <signal.h>

int run = 1;

/* Signal Handler for SIGINT */
void sigHandler(int signo)
{
    run = 0;
    printf("\nshutting down the program...\n");
    signal(SIGINT,SIG_DFL);
    signal(SIGTERM,SIG_DFL);
}


/*
 * Returns the number of occurrences of the string str found in
 * the program arguments.
 */
int get_number_of(int argc, char** argv, const char *str)
{
    int i;
    int count = 0;

    for (i=1; i<argc; i++) {
        if ( strcmp(argv[i], str) == 0 )
            count++;
    }

    return count;
}


/*
 * Parses the command-line arguments (GPIO pins) and fill the pssg structures
 * A negative attribute means that it is not in use
 * It returns a negative value if there are wrong arguments
 */
int parser(int argc, char **argv, pssg_t *pssg)
{
    int i, j, number_of_pssgs;

    // the arguments should start with pssg ID
    if ( strcmp(argv[1], "--id") != 0 ) {
        return RETURN_FAILURE;
    }

    // number of pssg in this controller
    number_of_pssgs = get_number_of(argc, argv, "--id");

    // initialization: a negative value means not in use.
    for (i = 0; i < number_of_pssgs; i++) {
        pssg[i].id = UNDEFINED;
        pssg[i].i0In = UNDEFINED;
        pssg[i].i1In = UNDEFINED;
        pssg[i].o0In = UNDEFINED;
        pssg[i].o1In = UNDEFINED;
        pssg[i].button = UNDEFINED;
        pssg[i].state = UNDEFINED;
    }

    /* Parse the arguments and fills the pssg structures.
     *
     * Each "--id" determines different passages
     * Arguments preceding the "--id" are related to the passage GPIOs
     *
     * 'j' is the pssg structure index. Each "--id" found in the arguments,
     * should increase the index because it means another passage
     */
    j = -1; // 'j' is the pssg struct index

    for (i=1; i<argc; i+=2) { // argument(i) value(i+1) argument(i+2)
         if ( strcmp(argv[i], "--id") == 0 ) {
             j++; // increase the index for each pssg.
                  // whenever it finds an "id" is another passage
             pssg[j].id = atoi(argv[i+1]);
         }
         if ( strcmp(argv[i], "--i0In") == 0 )
             pssg[j].i0In = atoi(argv[i+1]);
         if ( strcmp(argv[i], "--i1In") == 0 )
             pssg[j].i1In = atoi(argv[i+1]);
         if ( strcmp(argv[i], "--o0In") == 0 )
             pssg[j].o0In = atoi(argv[i+1]);
         if ( strcmp(argv[i], "--o1In") == 0 )
             pssg[j].o1In = atoi(argv[i+1]);
         if ( strcmp(argv[i], "--bttnIn") == 0 )
             pssg[j].button = atoi(argv[i+1]);
         if ( strcmp(argv[i], "--stateIn") == 0 )
             pssg[j].state = atoi(argv[i+1]);
         if ( strcmp(argv[i], "--bzzrOut") == 0 )
             pssg[j].buzzer = atoi(argv[i+1]);
         if ( strcmp(argv[i], "--rlseOut") == 0 )
             pssg[j].release = atoi(argv[i+1]);
    }

    return RETURN_SUCCESS;
}


/*
 * Export the GPIO to userspace. On success it returns 0, else returns -1
 */
int export_gpio(unsigned int gpio) 
{
    int fd, len;
    char str_gpio[10];
    
    if ((fd = open("/sys/class/gpio/export", O_WRONLY )) < 0 ) {
        fprintf(stderr,"Error(%d) opening /sys/class/gpio/export: %s\n", errno, strerror(errno));
        return RETURN_FAILURE;
    }

    // get the length of the gpio string
    len = sprintf(str_gpio, "%d", gpio);

    if ( write(fd, str_gpio, len) == 0) {
        fprintf(stderr,"Error(%d) writing /sys/class/gpio/export: %s\n", errno, strerror(errno));
        return RETURN_FAILURE;
    }

    close(fd);
    return RETURN_SUCCESS; // success GPIO exported

}


/*
 * Reverses the effect of exporting the GPIO to userspace.
 * On success it returns 0, else returns -1
 */
int unexport_gpio(unsigned int gpio) 
{
    int fd, len;
    char str_gpio[10];
    
    if ((fd = open("/sys/class/gpio/unexport", O_WRONLY )) < 0 ) {
        fprintf(stderr,"Error(%d) opening /sys/class/gpio/export: %s\n", errno, strerror(errno));
        return RETURN_FAILURE;
    }

    // get the length of the gpio string
    len = sprintf(str_gpio, "%d", gpio);

    if ( write(fd, str_gpio, len) == 0) {
        fprintf(stderr,"Error(%d) writing /sys/class/gpio/uexport: %s\n", errno, strerror(errno));
        return RETURN_FAILURE;
    }

    close(fd);
    return RETURN_SUCCESS; // success GPIO removed from userspace

}


/*
 * Set the gpio direction: IN(1) or OUT(0)
 * It returns 0 on success
 */
int gpio_set_direction(unsigned int gpio, unsigned int direction)
{
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


/* 
 * Select the signal edge that will make poll-on the "value" file return.
 * It returns 0 on success
 * ++ In a near future, this function will be implemented in Python ++
 */
int gpio_set_edge(unsigned int gpio, unsigned int edge) 
{
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


/* Export used GPIOs to the userspace, set direction and trigger edge */
int set_gpio_pins (pssg_t *pssg, int number_of_pssgs)
{
    int i;

    for (i = 0; i < number_of_pssgs; i++) {
        if (pssg[i].i0In != UNDEFINED) {
            if ( export_gpio(pssg[i].i0In) == RETURN_FAILURE ) return RETURN_FAILURE;
            if ( gpio_set_direction(pssg[i].i0In, IN) == RETURN_FAILURE ) return RETURN_FAILURE;
            if ( gpio_set_edge(pssg[i].i0In, FALLING) == RETURN_FAILURE ) return RETURN_FAILURE;
        }
        if (pssg[i].i1In != UNDEFINED) {
            if ( export_gpio(pssg[i].i1In) == RETURN_FAILURE ) return RETURN_FAILURE;
            if ( gpio_set_direction(pssg[i].i1In, IN) == RETURN_FAILURE ) return RETURN_FAILURE;
            if ( gpio_set_edge(pssg[i].i1In, FALLING) == RETURN_FAILURE ) return RETURN_FAILURE;
        }
        if (pssg[i].o0In != UNDEFINED) {
            if ( export_gpio(pssg[i].o0In) == RETURN_FAILURE ) return RETURN_FAILURE;
            if ( gpio_set_direction(pssg[i].o0In, IN) == RETURN_FAILURE ) return RETURN_FAILURE;
            if ( gpio_set_edge(pssg[i].o0In, FALLING) == RETURN_FAILURE ) return RETURN_FAILURE;
        }
        if (pssg[i].o1In != UNDEFINED) {
            if ( export_gpio(pssg[i].o1In) == RETURN_FAILURE ) return RETURN_FAILURE;
            if ( gpio_set_direction(pssg[i].o1In, IN) == RETURN_FAILURE ) return RETURN_FAILURE;
            if ( gpio_set_edge(pssg[i].o1In, FALLING) == RETURN_FAILURE ) return RETURN_FAILURE;
        }
        if (pssg[i].button != UNDEFINED) {
            if ( export_gpio(pssg[i].button) == RETURN_FAILURE ) return RETURN_FAILURE;
            if ( gpio_set_direction(pssg[i].button, IN) == RETURN_FAILURE ) return RETURN_FAILURE;
            if ( gpio_set_edge(pssg[i].button, RISING) == RETURN_FAILURE ) return RETURN_FAILURE;
        }
        if (pssg[i].state != UNDEFINED) {
            if ( export_gpio(pssg[i].state) == RETURN_FAILURE ) return RETURN_FAILURE;
            if ( gpio_set_direction(pssg[i].state, IN) == RETURN_FAILURE ) return RETURN_FAILURE;
            if ( gpio_set_edge(pssg[i].state, BOTH) == RETURN_FAILURE ) return RETURN_FAILURE;
        }
        if (pssg[i].buzzer != UNDEFINED) {
            if ( export_gpio(pssg[i].buzzer) == RETURN_FAILURE ) return RETURN_FAILURE;
            if ( gpio_set_direction(pssg[i].buzzer, OUT) == RETURN_FAILURE ) return RETURN_FAILURE;
        }
        if (pssg[i].release != UNDEFINED) {
            if ( export_gpio(pssg[i].release) == RETURN_FAILURE ) return RETURN_FAILURE;
            if ( gpio_set_direction(pssg[i].release, OUT) == RETURN_FAILURE ) return RETURN_FAILURE;
        }

    }

    return RETURN_SUCCESS;
}

/* Remove all GPIOs from userspace */
int unset_gpio_pins (pssg_t *pssg, int number_of_pssgs)
{
    int i;
   
    for (i = 0; i < number_of_pssgs; i++) {
        if (pssg[i].i0In != UNDEFINED)
            if ( unexport_gpio(pssg[i].i0In) == RETURN_FAILURE ) return RETURN_FAILURE;
        if (pssg[i].i1In != UNDEFINED)
            if ( unexport_gpio(pssg[i].i1In) == RETURN_FAILURE ) return RETURN_FAILURE;
        if (pssg[i].o0In != UNDEFINED)
            if ( unexport_gpio(pssg[i].o0In) == RETURN_FAILURE ) return RETURN_FAILURE;
        if (pssg[i].o1In != UNDEFINED)
            if ( unexport_gpio(pssg[i].o1In) == RETURN_FAILURE ) return RETURN_FAILURE;
        if (pssg[i].button != UNDEFINED)
            if ( unexport_gpio(pssg[i].button) == RETURN_FAILURE ) return RETURN_FAILURE;
        if (pssg[i].state != UNDEFINED)
            if ( unexport_gpio(pssg[i].state) == RETURN_FAILURE ) return RETURN_FAILURE;
        if (pssg[i].buzzer != UNDEFINED)
            if ( unexport_gpio(pssg[i].buzzer) == RETURN_FAILURE ) return RETURN_FAILURE;
        if (pssg[i].release != UNDEFINED)
            if ( unexport_gpio(pssg[i].release) == RETURN_FAILURE ) return RETURN_FAILURE;
    }

    return 0;
}


/*
 * This function runs as a thread and is lunched by "start_readers" function. It writes 0
 * in a register if it is listening the line D0, or ir writes 1 if it is listening D1. It counts
 * 26bits acording to the wiegand protocol.
 */
void *read_card (void *args) 
{
    char filename[40];
    char str_card_number[8];
    char message[50];
    int i; // for cicle index
    int fd[2]; // array of GPIO value file descriptors
    int epfd; // epool file descriptor
    int card_number;
    int mask;
    struct epoll_event ev[2];
    struct epoll_event events[2];   // 
    struct read_card_args *arg = (struct read_card_args*) args; // arguments passed to the thread
                                                                // It needs to be casted
    int gpio[] = {arg->d0, arg->d1};

    /* create a new epool instance and store the epool descriptor in epfd*/
    epfd = epoll_create(1);
    if (epfd == -1) {
        fprintf(stderr,"Error(%d) creating the epoll: %s\n", errno, strerror(errno));
        exit(EXIT_FAILURE);
    }

    /* get the two GPIO value file descriptors and register them the epoll instance referred to by the file descriptor epfd*/
    for (i=0; i<2; i++) {
        sprintf(filename, "/sys/class/gpio/gpio%d/value", gpio[i]);
        fd[i] = open(filename, O_RDWR | O_NONBLOCK);
        if (fd[i] == -1) {
            fprintf(stderr,"Error(%d) opening %s: %s\n", errno, filename, strerror(errno));
            exit(EXIT_FAILURE);
        }
        ev[i].events = EPOLLIN | EPOLLET | EPOLLPRI;
        ev[i].data.fd = fd[i];
        /* Add the file descriptors to the interest list for epfd */
        epoll_ctl(epfd, EPOLL_CTL_ADD, fd[i], &ev[i]);
    }

    epoll_wait(epfd, events, 2, 0);  // first time it triggers with current state, so ignore it

    while (run) {
        mask = 33554432;    // mask initialitation: 00000010000000000000000000000000
                            // It will be shifted to the right 26 times (one per bit)

        card_number = 0;    // card number initialization

        while (mask != 0 && run) {
            if ( epoll_wait(epfd, events, 2, EPOLL_WAIT_TIME) ) {   // wait for an evente. Only fetch up one event
                if (events[0].data.fd == fd[1]) // if the event was a D1, add 1 to the card number buffer and shift the mask
                    card_number = card_number | mask;
                mask = mask >> 1;   // if the event was D0, only shift the mask 
            }
        }

        if(run) {

            /* If the mask is 0, the mask has been shifted 26 time, therefore the card has been read completely.
             * It is time to generate the card number, put this number in the OS queue, wait a short
             * time and clean the mask and the card number buffer. 
             */

            // deregister the target file descriptors from the epoll instance referred by epfd. Future events will be ignored
            for (i=0; i<2; i++)  {
                epoll_ctl(epfd, EPOLL_CTL_DEL, fd[i], &ev[i]);
            }

            /* generate the card number
             * card number = (xxxxxxxxxxxxxxxxxxxxxxxxxx AND 01111111111111111111111110) >> 1
             */
            card_number = (card_number & 33554430) >> 1;
        
            // preparing the queue message for sending
            sprintf(message, "%d;%c;card=%08d", arg->pssg_id, arg->side, card_number);

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

            epoll_wait(epfd, events, 2, 0);  // first time it triggers with current state, so ignore it
        }
    }

    /* execute this code when the program exits */
    /* close all opened descriptors */
    for (i=0; i<2; i++) 
        close(fd[i]);
    
    return NULL;
}


/*
 * This function starts one thread per reader.
 * Each thread reads the card reader lines (D0 and D1), form the card number and
 * put into the queue a message with: pssgID+reader+card number
 */
int start_readers(int number_of_pssgs, int number_of_readers, pssg_t *pssg, pthread_t *r_thread, mqd_t mq) 
{
    int i; // array index
    struct read_card_args *args; // thread arguments

    /* Define an array of arguments. One argument struct per card reader */
    args = (struct read_card_args *)malloc(sizeof(struct read_card_args) * number_of_readers);

    for (i=0 ; i<number_of_pssgs; i++) {
        if (pssg[i].i0In != UNDEFINED && pssg[i].i1In != UNDEFINED ) { // if the pssg has input card reader
            /* fill the structure */
            args->pssg_id = pssg[i].id;
            args->d0 = pssg[i].i0In;
            args->d1 = pssg[i].i1In;
            args->side = '1';
            args->mq = mq;

            /* and launch the thread */
            pthread_create(r_thread, NULL, read_card, (void *)args);
            r_thread++;
            args++;
        }
        if (pssg[i].o0In != UNDEFINED && pssg[i].o1In != UNDEFINED ) { // if the pssg has output card reader
            /* fill the structure */
            args->pssg_id = pssg[i].id;
            args->d0 = pssg[i].o0In;
            args->d1 = pssg[i].o1In;
            args->side = '0';
            args->mq = mq;

            /* and launch the thread */
            pthread_create(r_thread, NULL, read_card, (void *)args);

            r_thread++;
            args++;
        }

    }

    return RETURN_SUCCESS;
}


void *buttons (void *b_args) 
{
    char filename[40];
    char message[50];
    char value[2] = {'0','\0'};
    int **bttn_tbl;
    int i;  // for cicle index
    int j=0;    // table row index: max value is the (number_of_buttons - 1)
    int epfd; // epool file descriptor
    struct epoll_event *ev;
    struct epoll_event *events;
    struct buttons_args *args = (struct buttons_args*) b_args;

    ev = (struct epoll_event *)malloc(sizeof(struct epoll_event) * args->number_of_buttons);
    events = (struct epoll_event *)malloc(sizeof(struct epoll_event) * args->number_of_buttons);

    /* Allocate memory for a table. The table has 2 columns and many rows as the number of buttons.
     * Column 1: pssg_ID; Column 2: file descriptor of the GPIO button
     */
    bttn_tbl = (int **) malloc(sizeof(int *) * args->number_of_buttons);
    for (i=0; i<(args->number_of_buttons); i++)
        bttn_tbl[i] = (int *) malloc(sizeof(int) * 2);

    // create a new epool instance
    epfd = epoll_create(1);
    if (epfd == -1) {
        fprintf(stderr,"Error(%d) creating the epoll: %s\n", errno, strerror(errno));
        exit(EXIT_FAILURE);
    }

    /* fill the table with pssg id and the file descriptor of button GPIO */
    for (i=0; i < (args->number_of_pssgs); i++) {
        if (args->pssg[i].button != UNDEFINED) {    // if the pssg has button
            bttn_tbl[j][0] = args->pssg[i].id;      // save the pssg id in the first col of the table

            // save the button fd in the second column of the table
            sprintf(filename, "/sys/class/gpio/gpio%d/value", args->pssg[i].button);
            bttn_tbl[j][1] = open(filename, O_RDWR | O_NONBLOCK);
            if (bttn_tbl[j][1] == -1) {
                fprintf(stderr,"Error(%d) opening %s: %s\n", errno, filename, strerror(errno));
                exit(EXIT_FAILURE);
            }

            ev[j].events = EPOLLIN | EPOLLET | EPOLLPRI;
            ev[j].data.fd = bttn_tbl[j][1];
            // Add the file descriptor to the interest list for epfd
            epoll_ctl(epfd, EPOLL_CTL_ADD, bttn_tbl[j][1], &ev[j]); 

            j++;

        }
    }
 
    epoll_wait(epfd, events, args->number_of_buttons, -1);  // first time it triggers with current state, so ignore it

    while (run) {
        if (epoll_wait(epfd, events, args->number_of_buttons, EPOLL_WAIT_TIME)) { // wait for an evente. Only fetch up one event
            for (j=0; j < args->number_of_buttons; j++) {
                if (events[0].data.fd == bttn_tbl[j][1]) {
                    // deregister the target file descriptor from the epoll instance to avoid button bounce
                    epoll_ctl(epfd, EPOLL_CTL_DEL, bttn_tbl[j][1], &ev[j]);
                    
                    usleep(BOUNCE_TIME);
                    read(bttn_tbl[j][1], value, 1);
                    lseek(bttn_tbl[j][1],0,SEEK_SET);

                    printf("VALOR %s\n",value);

                    if (strcmp(value, "1") == 0) {
                        printf("AAAAAAAAAAAAAAAAAAAAAAAA\n");
                        sprintf(message, "%d;0;button=1", bttn_tbl[j][0]);
                        // put the message into the queue
                        mq_send(args->mq, message, strlen(message), 1); // the '\0' is not sent in the queue
                        printf("%s\n", message);
                    }

                    // wait a bounce time and then register again the target file descriptor.
                    epoll_ctl(epfd, EPOLL_CTL_ADD, bttn_tbl[j][1], &ev[j]);
                    // because it was registered again, first time it triggers with current state, so ignore it again
                    epoll_wait(epfd, events, 1, -1);
                    break;
                }
            }
        }
    }

    return NULL;
}


void *state (void *s_args)
{
    char filename[40];
    char message[50];
    char value[2] = {0,'\0'};
    int **state_tbl;
    int i;
    int j=0;
    int epfd; // epool file descriptor
    struct epoll_event *ev;
    struct epoll_event *events;
    struct state_args *args = (struct state_args*) s_args;

    ev = (struct epoll_event *)malloc(sizeof(struct epoll_event) * args->number_of_states);
    events = (struct epoll_event *)malloc(sizeof(struct epoll_event) * args->number_of_states);

    /* Allocate memory for a table. The table has 2 columns and many rows as number of states.
     * Column 1: the pssg_ID; Column 2: file descriptor of the GPIO value.
     */
    state_tbl = (int **) malloc(sizeof(int *) * args->number_of_states);
    for (i=0; i<(args->number_of_states); i++)
        state_tbl[i] = (int *) malloc(sizeof(int) * 2);

    // create a new epool instance
    epfd = epoll_create(1);
    if (epfd == -1) {
        fprintf(stderr,"Error(%d) creating the epoll: %s\n", errno, strerror(errno));
        exit(1);
    }

    for (i=0; i < (args->number_of_pssgs); i++) {
        if (args->pssg[i].state != UNDEFINED) {     // if the pssg has state
            state_tbl[j][0] = args->pssg[i].id; // save the pssg id in the first col of the table

            // save the button fd in the second col of the table
            sprintf(filename, "/sys/class/gpio/gpio%d/value", args->pssg[i].state);
            state_tbl[j][1] = open(filename, O_RDWR | O_NONBLOCK);
            if (state_tbl[j][1] == -1) {
                fprintf(stderr,"Error(%d) opening %s: %s\n", errno, filename, strerror(errno));
                exit(EXIT_FAILURE);
            }

            ev[j].events = EPOLLIN | EPOLLET | EPOLLPRI;
            ev[j].data.fd = state_tbl[j][1];
            // Add the file descriptor to the interest list for epfd
            epoll_ctl(epfd, EPOLL_CTL_ADD, state_tbl[j][1], &ev[j]); 

            j++;

        }
    }
 
    epoll_wait(epfd, events, args->number_of_states, -1);  // first time it triggers with current state, so ignore it
   
    while (run) {
        if (epoll_wait(epfd, events, args->number_of_states, EPOLL_WAIT_TIME)) { // wait for an event
            for (j=0; j < args->number_of_states; j++) {
                if (events[0].data.fd == state_tbl[j][1]) {
                    // deregister the target file descriptor from the epoll instance to avoid button bounce
                    epoll_ctl(epfd, EPOLL_CTL_DEL, state_tbl[j][1], &ev[j]);
                    read(state_tbl[j][1], value, 1);
                    lseek(state_tbl[j][1],0,SEEK_SET);
                    sprintf(message, "%d;0;state=%s", state_tbl[j][0], value);
                    // put the message into the queue
                    mq_send(args->mq, message, strlen(message), 1); // the '\0' caracter is not sent in the queue
                    printf("%s\n", message);
                    // wait a bounce time and then register again the target file descriptor.
                    usleep(BOUNCE_TIME);
                    epoll_ctl(epfd, EPOLL_CTL_ADD, state_tbl[j][1], &ev[j]);
                    // because it was registered again, first time it triggers with current state, so ignore it again
                    epoll_wait(epfd, events, 1, -1);
                    break;
                }
            }
        }
    }

    return NULL;
}

