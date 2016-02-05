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
    pssg_t *pssg; // array of pointers to pssg type structures
    pthread_t *r_thread; // array of pointers to all threads created by this program
    pthread_t b_thread; //
    pthread_t s_thread; //
    int i; // auxiliar variable used in cicles
    int number_of_pssgs = 0;
    int number_of_readers = 0;
    int number_of_buttons = 0;
    int number_of_states = 0;
    mqd_t mq; // message queue
    struct buttons_args b_args;
    struct state_args s_args;

    //
    signal(SIGINT, sigHandler);
    signal(SIGTERM, sigHandler);

    /* open the message queue only for sending message to the main process
     * It must be created by the main process
     */
    if ( (mq = mq_open(QUEUE_NAME, O_WRONLY)) == RETURN_FAILURE ) { 
        printf("Error opening the message queue: %s\n", strerror(errno));
        exit(EXIT_FAILURE);
    }

    // get number of pssgs from arguments
    number_of_pssgs = get_number_of(argc, argv, "--id");
    // get number of readers
    number_of_readers = get_number_of(argc, argv, "--i0In") + get_number_of(argc, argv, "--o0In");
    // get number of buttons
    number_of_buttons = get_number_of(argc, argv, "--bttnIn");
    // get number of state pins
    number_of_states = get_number_of(argc, argv, "--stateIn");


    // array with all reader threads
    r_thread = (pthread_t *) malloc(sizeof(pthread_t) * number_of_readers);

    /* Array of pssg struct. Each struct stores the GPIO numbers used in the passage.
     * The array is filled with the parser function
     */
    pssg = (pssg_t *)malloc(sizeof(pssg_t) * number_of_pssgs);
    if ( parser(argc, argv, pssg) == RETURN_FAILURE ) {
        printf("Error: You should declare a pssg ID before declaring GPIO pins\n");
        exit(EXIT_FAILURE);
    }

    // set all GPIO pins
    if ( set_gpio_pins(pssg, number_of_pssgs) == RETURN_FAILURE ) {
        printf("Error setting GPIO pins. Program aborted\n");
        exit(EXIT_FAILURE);
    }

    /* Start listening the card readers.
     * Threads send to the main process a message with pssg ID + card reader ID + card number
     */
    start_readers(number_of_pssgs, number_of_readers, pssg, r_thread, mq);

    /* Catch button pushes.
     * One thread for all system buttons
     */
    b_args.number_of_pssgs = number_of_pssgs;
    b_args.number_of_buttons = number_of_buttons;
    b_args.pssg = pssg;
    b_args.mq = mq;
    pthread_create(&b_thread, NULL, buttons, (void *)&b_args);

    /* Catch the state changes. The passage could change its state from closed to open
     * or vice versa. One thread listen for all passages */
    s_args.number_of_pssgs = number_of_pssgs;
    s_args.number_of_states = number_of_states;
    s_args.pssg = pssg;
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
    if ( unset_gpio_pins(pssg, number_of_pssgs) == -1 ) {
        printf("Error removing GPIO pins from userspace");
        exit(EXIT_FAILURE);
    }

    return RETURN_SUCCESS;
}

