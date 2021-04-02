#include <gpiod.h>
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
#include <state_snsr.h>




int init_state_snsr(state_snsr_t *state_snsr_p,
                struct gpiod_chip *chip,
                unsigned int gpio_num,
                unsigned int door_id,
                struct timespec *event_wait_time_p){

    sd_journal_print(LOG_NOTICE, "State Sensor of Door: %d using GPIO: %d\n",
                     door_id, gpio_num);
    state_snsr_p->chip = chip;
    state_snsr_p->gpio_num = gpio_num;
    state_snsr_p->door_id = door_id;
    state_snsr_p->event_wait_time_p = event_wait_time_p;
}




int enable_state_snsr(state_snsr_t *state_snsr_p) {
    int ret = RETURN_SUCCESS;

    // Getting the GPIO line for the state sensor.
    state_snsr_p->b_line = gpiod_chip_get_line(state_snsr_p->chip, state_snsr_p->gpio_num);
    if (!state_snsr_p->b_line) {
        sd_journal_print(LOG_ALERT, "Error getting line of GPIO: %d for State Sensor of Door: %d\n",
                         state_snsr_p->gpio_num, state_snsr_p->door_id);
        return RETURN_FAILURE;
    }

    // Registering the lines to generate events on both edges (falling and raising).
    // This is the way that the sensor indicates state changes in the door.
    ret = gpiod_line_request_both_edges_events(state_snsr_p->b_line, CONSUMER);
    if (ret < 0) {
        sd_journal_print(LOG_ALERT, "Failing to request event notification for State Sensor of Door: %d\n",
                         state_snsr_p->door_id);
        return RETURN_FAILURE;
    }
    return ret;
}




// The following is the thread which detects when the state sensor changes its state and
// send this event with the door id to the python process using the the posix message queue.
// There is one thread of this for each state sensor.
void *run_state_snsr (void *arg_p){
    state_snsr_t *state_snsr_p = (state_snsr_t *) arg_p;
    char q_msg [50];
    int current_state, new_state;
    int ret;

    // Enable the line checking if it is not used by another process.
    // If it is used, notify all threads to finish and set the main
    // returned value as FAILURE.
    if (RETURN_FAILURE == enable_state_snsr(state_snsr_p)) {
        exit_flag = FINISH;
        return_exit = RETURN_FAILURE;
    }


    // Getting the actual state
    // As this is the same hardware of buttons and we want closed == 1 and
    // opened == 0, the value read is inverted
    current_state = ! gpiod_line_get_value(state_snsr_p->b_line);

    while (!exit_flag) {

        // Waiting "event_wait_time" for falling or raising edge events in the line
        ret = gpiod_line_event_wait(state_snsr_p->b_line, state_snsr_p->event_wait_time_p);

        switch (ret) {

            // ret == 1 means an event happened before timout (event_wait_time)
            case 1:
                // Clean the event reading it. If we do not do that, the next call
                // to gpiod_line_event_wait will trigger again (dont remember)
                ret = gpiod_line_event_read(state_snsr_p->b_line, &state_snsr_p->event);
                // Release the line to avoid more events caused by bounce.
                gpiod_line_release(state_snsr_p->b_line);
                // Sleep until bounce finished
                usleep(BOUNCE_TIME);

                // Enable the line again checking if it is not used by another process.
                // If it is used, notify all threads to finish and set the main
                // returned value as FAILURE.
                if (RETURN_FAILURE == enable_state_snsr(state_snsr_p)) {
                    exit_flag = FINISH;
                    return_exit = RETURN_FAILURE;
                }

                // Get the value of the line after bounce finished
                new_state = ! gpiod_line_get_value(state_snsr_p->b_line);

                // If the value of new_state is different of the current_state, it means
                // a real change in the state (not noise)
                if (new_state != current_state) {
                    current_state = new_state;
                    sd_journal_print(LOG_NOTICE, "State Sensor of Door: %d detected state: %d\n",
                                     state_snsr_p->door_id, current_state);
                    // Creating the string that is going to be sent to the message queue.
                    sprintf(q_msg, "%d;0;state=%d", state_snsr_p->door_id, current_state);
                    // As many thread can write at the same time in message queue, it is protected with
                    // a mutex. Maybe the same queue is itself protected, but I don't know.
                    pthread_mutex_lock(&mq_mutex);
                        ret = mq_send(mq, q_msg, strlen(q_msg), 1);
                    pthread_mutex_unlock(&mq_mutex);
                        if (ret == RETURN_SUCCESS)
                            sd_journal_print(LOG_INFO, "SUCCESS Sending to queue: %s\n", q_msg);
                        else
                            sd_journal_print(LOG_ALERT, "ERROR Sending to queue: %s\n", q_msg);
                }
                else
                    sd_journal_print(LOG_INFO, "Noise in State Sensor of Door: %d\n", state_snsr_p->door_id);
                break;

            // ret == 0 means "event_wait_time" happened and there wasn't any event. In this case
            // nothing is done, and "exit_flag" is checked again at the begining of while loop
            case 0:
                sd_journal_print(LOG_DEBUG, "Thread of State Sensor of Door: %d checking for exit\n", state_snsr_p->door_id);
                break;

            // This would be an unknown error.
            default:
                sd_journal_print(LOG_WARNING, "Unknown error on thread of State Sensor of Door: %d\n", state_snsr_p->door_id);
        }

    }

    // When finsih_handler ask to finish setting "exit_flag", before
    // finishing, the line used by the state sensor is released.
    sd_journal_print(LOG_NOTICE, "Thread of State Sensor of Door: %d releasing GPIO: %d\n", state_snsr_p->door_id, state_snsr_p->gpio_num);
    gpiod_line_release(state_snsr_p->b_line);
    sd_journal_print(LOG_NOTICE, "Thread of State Sensor of Door: %d finished.", state_snsr_p->door_id);
}
