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


int main(int argc, char** argv) 
{
    pssg_t *pssg; // array of pointers to pssg type structures
    pthread_t *thread; // array of pointers to all threads created by this program
    pthread_t b_thread; //
    int i; // auxiliar variable used in for cicles
    int number_of_pssgs = 0;
    int number_of_readers = 0;
    int number_of_buttons = 0;
    int number_of_states = 0;
    int number_of_threads;
    mqd_t mq; // message queue
    struct buttons_args b_args;
    struct state_args s_args;

    // open the message queue only for sending message to the main process
    // It must be created by the main process
    if ( (mq = mq_open("/pssg_iface_queue", O_WRONLY)) == -1 ) {
        printf("Error opening the message queue: %s\n", strerror(errno));
        exit(1);
    }

    // get number of pssgs from arguments
    number_of_pssgs = get_number_of(argc, argv, "--id");
    // get number of readers
    number_of_readers = get_number_of(argc, argv, "--i0In") + get_number_of(argc, argv, "--o0In");
    // get number of buttons
    number_of_buttons = get_number_of(argc, argv, "--bttnIn");
    // get number of state pins
    number_of_states = get_number_of(argc, argv, "--stateIn");
    // number of thread: one thread per card reader, one for all button and one for all state pins
    number_of_threads = number_of_readers + 1 + 1;


    // array with all system threads
    thread = (pthread_t *) malloc(sizeof(pthread_t) * number_of_threads);

    /* array of pssg struct. Each struct store the pin numbers.
     * The array is filled with the parser function
     */
    pssg = (pssg_t *)malloc(sizeof(pssg_t) * number_of_pssgs);
    parser(argc, argv, pssg);


    /* set all GPIO pins */
    if ( set_gpio_pins(pssg, number_of_pssgs) == -1 ) {
        printf("Error setting GPIO pins. Program aborted");
        exit(1);
    }

    /* start listening the card readers and send to the main process a message with
     * pssg ID + card reader ID + card number
     */
    start_readers(number_of_pssgs, number_of_readers, pssg, thread, mq);

    /* start listening button pushes */
    b_args.number_of_pssgs = number_of_pssgs;
    b_args.number_of_buttons = number_of_buttons;
    b_args.pssg = pssg;
    b_args.mq = mq;
    pthread_create(&b_thread, NULL, buttons, (void *)&b_args);

    /* start listening state pins */
    s_args.number_of_pssgs = number_of_pssgs;
    s_args.number_of_states = number_of_states;
    s_args.pssg = pssg;
    s_args.mq = mq;
    pthread_create(&b_thread, NULL, state, (void *)&s_args);

    // waits  for  the  threads  to  terminate
    for (i = 0; i < number_of_threads; i++)
        pthread_join(thread[i], NULL);

    return 0;
}

