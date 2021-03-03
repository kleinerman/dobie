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


int exit_flag = 0;
mqd_t mq;
pthread_mutex_t mq_mutex;


int main(int argc, char **argv)
{
    struct gpiod_chip *chip = NULL;
    struct timespec event_wait_time = { 2, 0 };
    button_t *buttons_a;
    state_snsr_t *state_snsrs_a;
    reader_t *readers_a;
    int ret;
    int i; // auxiliar variable used in cicles
    int number_of_readers = 0;
    int number_of_buttons = 0;
    int number_of_state_snsrs = 0;
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
        sd_journal_print(LOG_CRIT, "This ioiface was not compiled for this controller. Exiting..\n");
        exit(EXIT_FAILURE);
    }


    /* open the message queue only for sending message to the main process
     * It must be created by the main process
     */
    if ( (mq = mq_open(QUEUE_NAME, (O_WRONLY | O_NONBLOCK) )) == RETURN_FAILURE ) {
        sd_journal_print(LOG_ALERT, "Error opening the message queue. Exiting..\n");
        exit(EXIT_FAILURE);
    }


    pthread_mutex_init(&mq_mutex, NULL);



    // get number of buttons
    number_of_buttons = get_number_of(argc, argv, "--bttn");
    // get number of state pins
    number_of_state_snsrs = get_number_of(argc, argv, "--state");
    // get number of readers
    number_of_readers = get_number_of(argc, argv, "--inRdr") + get_number_of(argc, argv, "--outRdr");


    // Open the GPIO Chip
    chip = gpiod_chip_open_by_name(CHIP_NAME);
    if (!chip) {
        sd_journal_print(LOG_ALERT, "Error trying to open GPIO chip: %s\n", CHIP_NAME);
        exit(EXIT_FAILURE);
    }


    //Asking memory for buttons
    buttons_a = (button_t *)malloc(sizeof(button_t) * number_of_buttons);
    state_snsrs_a = (state_snsr_t *)malloc(sizeof(state_snsr_t) * number_of_state_snsrs);
    readers_a = (reader_t *)malloc(sizeof(reader_t) * number_of_readers);


    //Filling button structures, state structures and card_readers structures with
    //the parametters received as arguments
    init_perif(argc, argv, chip, &event_wait_time, buttons_a, state_snsrs_a, readers_a);


    //Before creating the threads, overwritting SIGINT and SIGTERM signals
    signal(SIGINT, finish_handler);
    signal(SIGTERM, finish_handler);


    //Starting buttons threads
    for (i=0; i<number_of_buttons; i++) {
        pthread_create(&(buttons_a[i].b_thread), NULL, run_button, (void *)&buttons_a[i]);
    }

    //Starting state sensors threads
    for (i=0; i<number_of_state_snsrs; i++) {
        pthread_create(&(state_snsrs_a[i].b_thread), NULL, run_state_snsr, (void *)&state_snsrs_a[i]);
    }

    //Starting reader threads
    for (i=0; i<number_of_readers; i++) {
        pthread_create(&(readers_a[i].r_thread), NULL, run_reader, (void *)&readers_a[i]);
    }


    //Joining buttons threads
    for (i=0; i<number_of_buttons; i++) {
        pthread_join(buttons_a[i].b_thread, NULL);
    }


    //Joining state_snsrs threads
    for (i=0; i<number_of_state_snsrs; i++) {
        pthread_join(state_snsrs_a[i].b_thread, NULL);
    }

    //Joining readers threads
    for (i=0; i<number_of_readers; i++) {
        pthread_join(readers_a[i].r_thread, NULL);
    }


    return RETURN_SUCCESS;

}
