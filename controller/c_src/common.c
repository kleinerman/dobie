#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <systemd/sd-journal.h>
#include <pthread.h>
#include <mqueue.h>
#include <unistd.h>
#include <signal.h>
#include <common.h>
#include <button.h>
#include <state_snsr.h>
#include <reader.h>



void finish_handler(int sig_num)
{
    sd_journal_print(LOG_NOTICE, "Main thread notifying all threads to finish");
    exit_flag = 1;
    signal(SIGINT,SIG_DFL);
    signal(SIGTERM,SIG_DFL);
}


/*
 * Returns the number of occurrences of the string str found in
 * the program arguments.
 */
int get_number_of(int argc, char **argv, const char *str)
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
 * Parses the command-line arguments (GPIO pins) and fill the door structures
 * A negative attribute means that it is not in use
 * It returns a negative value if there are wrong arguments
 */
int init_perif(int argc, char *argv[], struct gpiod_chip *chip_p,
               struct timespec *event_wait_time_p, button_t buttons_a[],
               state_snsr_t state_snsrs_a[], reader_t readers_a[]) {
    int i, j, door_id;
    int buttons_count = 0;
    int state_snsrs_count = 0;
    int readers_count = 0;

    // the arguments should start with door ID
    if ( strcmp(argv[1], "--id") != 0 ) {
        return RETURN_FAILURE;
    }

    for (i=1; i<argc; i+=2) { // argument(i) value(i+1) argument(i+2)
        if ( strcmp(argv[i], "--id") == 0 ) {
            door_id = atoi(argv[i+1]);
            continue;
        }
        if ( strcmp(argv[i], "--inRdr") == 0 ) {
            sd_journal_print(LOG_NOTICE, "Parameterizing data lines on Input Reader of Door: %d\n", door_id);
            init_reader(&(readers_a[readers_count]), chip_p, atoi(argv[i+1]), atoi(argv[i+2]), atoi(argv[i+3]), INPUT, door_id, event_wait_time_p);
            readers_count++;
            i+=2;
            continue;
        }

        if ( strcmp(argv[i], "--outRdr") == 0 ) {
            sd_journal_print(LOG_NOTICE, "Parameterizing data lines on Output Reader of Door: %d\n", door_id);
            init_reader(&(readers_a[readers_count]), chip_p, atoi(argv[i+1]), atoi(argv[i+2]), atoi(argv[i+3]), OUTPUT, door_id, event_wait_time_p);
            readers_count++;
            i+=2;
            continue;
        }

        if ( strcmp(argv[i], "--bttn") == 0 ) {
            sd_journal_print(LOG_NOTICE, "Parameterizing Button of Door: %d\n", door_id);
            init_button(&(buttons_a[buttons_count]), chip_p, atoi(argv[i+1]), door_id, event_wait_time_p);
            buttons_count++;
            continue;
        }
        if ( strcmp(argv[i], "--state") == 0 ) {
            sd_journal_print(LOG_NOTICE, "Parameterizing State Sensor of Door: %d\n", door_id);
            init_state_snsr(&(state_snsrs_a[state_snsrs_count]), chip_p, atoi(argv[i+1]), door_id, event_wait_time_p);
            state_snsrs_count++;
            continue;
        }
    }

    return RETURN_SUCCESS;
}
