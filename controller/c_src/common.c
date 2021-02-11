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
#include <signal.h>
#include <common.h>
#include <button.h>



void finish_handler(int sig_num)
{
    printf("Notifying all threads to finish..\n");
    exit_flag = 1;
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
 * Parses the command-line arguments (GPIO pins) and fill the door structures
 * A negative attribute means that it is not in use
 * It returns a negative value if there are wrong arguments
 */
int init_perif(int argc, char **argv, struct gpiod_chip* chip_p, struct timespec* event_wait_time_p, button_t buttons_a[]) {
    int i, j, door_id;
    int buttons_count = 0;

    // the arguments should start with door ID
    if ( strcmp(argv[1], "--id") != 0 ) {
        return RETURN_FAILURE;
    }

    for (i=1; i<argc; i+=2) { // argument(i) value(i+1) argument(i+2)
        if ( strcmp(argv[i], "--id") == 0 ) {
             door_id = atoi(argv[i+1]);
             printf("----------%d----------\n", door_id);
        }
        if ( strcmp(argv[i], "--i0In") == 0 )
            perror("nothing yet..");
        if ( strcmp(argv[i], "--i1In") == 0 )
            perror("nothing yet..");
        if ( strcmp(argv[i], "--o0In") == 0 )
            perror("nothing yet..");
        if ( strcmp(argv[i], "--o1In") == 0 )
            perror("nothing yet..");
        if ( strcmp(argv[i], "--bttnIn") == 0 ){
            printf("Initializing button of door: %d\n", door_id);
            init_button(&(buttons_a[buttons_count]), chip_p, atoi(argv[i+1]), door_id, event_wait_time_p);
            buttons_count++;
        }
        if ( strcmp(argv[i], "--stateIn") == 0 )
            perror("nothing yet..");
        if ( strcmp(argv[i], "--bzzrOut") == 0 )
            perror("nothing yet..");
        if ( strcmp(argv[i], "--rlseOut") == 0 )
            perror("nothing yet..");
    }

    return RETURN_SUCCESS;
}


