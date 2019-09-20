#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <sys/epoll.h>
#include <pthread.h>
#include <libioiface.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <mqueue.h>
#include <signal.h>

int main(int argc, char** argv) 
{
    door_t *door; // array of pointers to door type structures
    pthread_t *r_thread; // array of pointers to all threads created by this program
    pthread_t b_thread; //
    pthread_t s_thread; //
    int i; // auxiliar variable used in cicles
    int number_of_doors = 0;
    int number_of_readers = 0;
    int number_of_buttons = 0;
    int number_of_states = 0;
    mqd_t mq; // message queue
    struct buttons_args b_args;
    struct state_args s_args;
    char mac_string[MAC_STR_LEN] = ""; // Initializing all the array to /0
    FILE *sys_mac_file_ptr;


    /* When the stdout and stderr don't go to a terminal,
     * the C standard library buffers them. We need to avoid
     * this behaviour when we launch this program from python
     * using Popen and we want to redirect the output of this
     * program to a file
     */
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    //setvbuf(stdout, NULL, _IONBF, 0); //another way of do the above
    //setvbuf(stderr, NULL, _IONBF, 0); //
    
    //
    signal(SIGINT, sigHandler);
    signal(SIGTERM, sigHandler);


    if ((sys_mac_file_ptr = fopen(SYS_FILE_MAC, "r")) == NULL) {
        printf("Error opening mac file of sys filesystem\n");
        exit(EXIT_FAILURE);
    }

    fgets(mac_string, MAC_STR_LEN, sys_mac_file_ptr);
    /*mac_string will end up with the 17 chars of the MAC divided 
     * by ":" and at the end a "/0" char remaining of the initialization
    */

    fclose(sys_mac_file_ptr);

    if (strcmp(mac_string, MAC)) {
        printf("This ioiface was not compiled for this controller. Exiting..\n");
        exit(EXIT_FAILURE);
    }


    /* open the message queue only for sending message to the main process
     * It must be created by the main process
     */
    if ( (mq = mq_open(QUEUE_NAME, O_WRONLY)) == RETURN_FAILURE ) { 
        printf("Error opening the message queue: %s\n", strerror(errno));
        exit(EXIT_FAILURE);
    }

    // get number of doors from arguments
    number_of_doors = get_number_of(argc, argv, "--id");
    // get number of readers
    number_of_readers = get_number_of(argc, argv, "--i0In") + get_number_of(argc, argv, "--o0In");
    // get number of buttons
    number_of_buttons = get_number_of(argc, argv, "--bttnIn");
    // get number of state pins
    number_of_states = get_number_of(argc, argv, "--stateIn");


    // array with all reader threads
    r_thread = (pthread_t *) malloc(sizeof(pthread_t) * number_of_readers);

    /* Array of door struct. Each struct stores the GPIO numbers used in the door.
     * The array is filled with the parser function
     */
    door = (door_t *)malloc(sizeof(door_t) * number_of_doors);
    if ( parser(argc, argv, door) == RETURN_FAILURE ) {
        printf("Error: You should declare a door ID before declaring GPIO pins\n");
        exit(EXIT_FAILURE);
    }

    // set all GPIO pins
    if ( set_gpio_pins(door, number_of_doors) == RETURN_FAILURE ) {
        printf("Error setting GPIO pins. Program aborted\n");
        exit(EXIT_FAILURE);
    }

    /* Start listening the card readers.
     * Threads send to the main process a message with door ID + card reader ID + card number
     */
    start_readers(number_of_doors, number_of_readers, door, r_thread, mq);

    /* Catch button pushes.
     * One thread for all system buttons
     */
    b_args.number_of_doors = number_of_doors;
    b_args.number_of_buttons = number_of_buttons;
    b_args.door = door;
    b_args.mq = mq;
    pthread_create(&b_thread, NULL, buttons, (void *)&b_args);

    /* Catch the state changes. The door could change its state from closed to open
     * or vice versa. One thread listen for all doors */
    s_args.number_of_doors = number_of_doors;
    s_args.number_of_states = number_of_states;
    s_args.door = door;
    s_args.mq = mq;
    pthread_create(&s_thread, NULL, state, (void *)&s_args);

    /* This part of the code should run only if the application is closed
     *  wait  for  the  threads  to  terminate
     */
    for (i = 0; i < number_of_readers; i++)
        pthread_join(r_thread[i], NULL);
    pthread_join(b_thread, NULL);
    pthread_join(s_thread, NULL);

    // uset used GPIOs
    if ( unset_gpio_pins(door, number_of_doors) == -1 ) {
        printf("Error removing GPIO pins from userspace");
        exit(EXIT_FAILURE);
    }

    return RETURN_SUCCESS;
}

