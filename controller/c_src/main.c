#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <systemd/sd-journal.h>
#include <sys/epoll.h>
#include <pthread.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <mqueue.h>
#include <signal.h>
#include <gpiod.h>
#include <common.h>
#include <button.h>
#include <state_snsr.h>
#include <reader.h>


int exit_flag = NO_FINISH;
int return_exit = RETURN_SUCCESS;
mqd_t mq;
pthread_mutex_t mq_mutex;


int main(int argc, char **argv)
{
    struct gpiod_chip *chip = NULL;
    struct timespec event_wait_time = { 2, 0 };
    button_t *buttons_a; // To create an array of button strucutres
    state_snsr_t *state_snsrs_a; // To create an array of state sensors strucutres
    reader_t *readers_a; // To create an array of reader structures
    int number_of_readers = 0;
    int number_of_buttons = 0;
    int number_of_state_snsrs = 0;
    char mac_string[MAC_STR_LEN] = ""; // Initializing all the array to /0
    FILE *sys_mac_file_ptr; // File pointer to open MAC sys file
    int i; // auxiliar variable used in cicles


    // When the stdout and stderr don't go to a terminal,
    // the C standard library buffers them. We need to avoid
    // this behaviour when we launch this program from python
    // using Popen and we want to redirect the output of this
    // program to a file
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    //setvbuf(stdout, NULL, _IONBF, 0); //another way of do the above
    //setvbuf(stderr, NULL, _IONBF, 0); //


    // Opening MAC file in sys filesystem to read the MAC address
    if ((sys_mac_file_ptr = fopen(SYS_FILE_MAC, "r")) == NULL) {
        sd_journal_print(LOG_ALERT, "Error opening MAC file in sys filesystem. Exiting..\n");
        exit(EXIT_FAILURE);
    }

    // Saving the MAC address in mac_string array
    if (fgets(mac_string, MAC_STR_LEN, sys_mac_file_ptr) == NULL) {
        sd_journal_print(LOG_ALERT, "Error saving MAC string in array. Exiting..\n");
        exit(EXIT_FAILURE);
    }

    // Closing MAC file of sys filesystem
    fclose(sys_mac_file_ptr);

    // Checking if the MAC of sys filesystem is equal to macro set
    // by installation script.
    if (strcmp(mac_string, MAC)) {
        sd_journal_print(LOG_CRIT, "This ioiface was not compiled for this controller. Exiting..\n");
        exit(EXIT_FAILURE);
    }

    // Opening the message queue to send messages to python process.
    // As this queue is written by different threads, it is protected with a mutex.
    // It is opened in write only mode since it only used to send messages.
    // The documentation says that the flag O_NONBLOCK, causes the queue to be opened
    // in nonblocking mode and if a subsequent call to mq_receive() or mq_send()
    // can not be performed without blocking, the call will fail immediately with the
    // error EAGAIN. However in this case I am using this option because I noticed that
    // some messages sent to queue were not received from the other side if this option
    // is not enabled.
    if ( (mq = mq_open(QUEUE_NAME, (O_WRONLY | O_NONBLOCK) )) == RETURN_FAILURE ) {
        sd_journal_print(LOG_ALERT, "Error opening the message queue. Exiting..\n");
        exit(EXIT_FAILURE);
    }

    // Initing the mutex to protect the the previous message queue
    pthread_mutex_init(&mq_mutex, NULL);

    // get number of buttons
    number_of_buttons = get_number_of(argc, argv, "--bttn");
    // get number of state sensors
    number_of_state_snsrs = get_number_of(argc, argv, "--state");
    // get number of readers
    number_of_readers = get_number_of(argc, argv, "--inRdr") + get_number_of(argc, argv, "--outRdr");


    // Open the GPIO Chip
    chip = gpiod_chip_open_by_name(CHIP_NAME);
    if (!chip) {
        sd_journal_print(LOG_ALERT, "Error trying to open GPIO chip: %s\n", CHIP_NAME);
        exit(EXIT_FAILURE);
    }

    // Creating arrays of structures of buttons, state sensors and readers
    // according to the number of them calculated above.
    buttons_a = (button_t *)malloc(sizeof(button_t) * number_of_buttons);
    state_snsrs_a = (state_snsr_t *)malloc(sizeof(state_snsr_t) * number_of_state_snsrs);
    readers_a = (reader_t *)malloc(sizeof(reader_t) * number_of_readers);

    // Filling button structures, state structures and card_readers structures with
    // the parametters received as arguments
    init_perif(argc, argv, chip, &event_wait_time, buttons_a, state_snsrs_a, readers_a);

    // Before creating the threads, overwritting SIGINT and SIGTERM signals
    // to call finish_handler. In this function before calling the original
    // handler, "exit_flag" is set to 1 to inform all threads to finish.
    signal(SIGINT, finish_handler);
    signal(SIGTERM, finish_handler);


    // Starting buttons threads
    for (i=0; i<number_of_buttons; i++) {
        pthread_create(&(buttons_a[i].thread), NULL, run_button, (void *)&buttons_a[i]);
    }

    // Starting state sensors threads
    for (i=0; i<number_of_state_snsrs; i++) {
        pthread_create(&(state_snsrs_a[i].thread), NULL, run_state_snsr, (void *)&state_snsrs_a[i]);
    }

    // Starting reader threads
    for (i=0; i<number_of_readers; i++) {
        pthread_create(&(readers_a[i].thread), NULL, run_reader, (void *)&readers_a[i]);
    }

    //Joining buttons threads
    for (i=0; i<number_of_buttons; i++) {
        pthread_join(buttons_a[i].thread, NULL);
    }

    //Joining state_snsrs threads
    for (i=0; i<number_of_state_snsrs; i++) {
        pthread_join(state_snsrs_a[i].thread, NULL);
    }

    //Joining readers threads
    for (i=0; i<number_of_readers; i++) {
        pthread_join(readers_a[i].thread, NULL);
    }


    if (RETURN_FAILURE == return_exit) {
        sd_journal_print(LOG_ALERT, "Error trying to get some GPIO Lines. Exiting..\n");
        exit(EXIT_FAILURE);
    }

    return return_exit;
}
