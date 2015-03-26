#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <sys/epoll.h>
#include <pthread.h>
#include <access.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <mqueue.h>


int main(int argc, char** argv) {
    door_t *door; // array of pointers to door type structures
    pthread_t *thread; // array of pointers to all threads created by this program
    pthread_t b_thread; //
    int i; // auxiliar variable used in for cicles
    int number_of_doors = 0;
    int number_of_readers = 0;
    int number_of_buttons = 0;
    int number_of_state = 0;
    int number_of_threads;
    mqd_t mq; // message queue
    struct buttons_args b_args;

    // open the message queue only for sending message to the main process
    // It must be created by the main process
    if ( (mq = mq_open("/door_iface_queue", O_WRONLY)) == -1 ) {
        printf("Error opening the message queue: %s\n", strerror(errno));
        exit(1);
    }

    // get number of doors from arguments
    number_of_doors = get_number_of(argc, argv, "--id");
    // get number of readers
    number_of_readers = get_number_of(argc, argv, "--i0In") + get_number_of(argc, argv, "--o0In");
    // get number of buttons
    number_of_buttons = get_number_of(argc, argv, "--bttnIn");
    // get number of state pins
    number_of_state = get_number_of(argc, argv, "--stateIn");
    // number of thread: one thread per card reader, one for all button and one for all state pins
    number_of_threads = number_of_readers + 1 + 1;


    // array with all system threads
    thread = (pthread_t *) malloc(sizeof(pthread_t) * number_of_threads);

    /* array of door struct. Each struct store the pin numbers.
     * The array is filled with the parser function
     */
    door = (door_t *)malloc(sizeof(door_t) * number_of_doors);
    parser(argc, argv, door);

    /* start listening the card readers and send to the main process a message with
     * door ID + card reader ID + card number
     */
    start_readers(number_of_doors, number_of_readers, door, thread, mq);

    /* start listening button pushes */
    b_args.number_of_doors = number_of_doors;
    b_args.number_of_buttons = number_of_buttons;
    b_args.door = door;
    b_args.mq = mq;
    pthread_create(&b_thread, NULL, buttons, (void *)&b_args);


    // waits  for  the  threads  to  terminate
    for (i = 0; i < number_of_threads; i++)
        pthread_join(thread[i], NULL);

    return 0;
}

