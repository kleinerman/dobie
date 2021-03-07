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
#include <button.h>




int init_button(button_t *button_p,
                struct gpiod_chip *chip,
                unsigned int gpio_num,
                unsigned int door_id,
                struct timespec *event_wait_time_p){

    sd_journal_print(LOG_NOTICE, "Button of Door: %d using GPIO: %d\n",
                     door_id, gpio_num);
    button_p->chip = chip;
    button_p->gpio_num = gpio_num;
    button_p->door_id = door_id;
    button_p->event_wait_time_p = event_wait_time_p;
}




int enable_button(button_t *button_p) {
    int ret = 0;

    // Getting the GPIO line for the button.
    button_p->b_line = gpiod_chip_get_line(button_p->chip, button_p->gpio_num);
    if (!button_p->b_line) {
        sd_journal_print(LOG_ALERT, "Error getting line of GPIO: %d for Button of Door: %d\n",
                         button_p->gpio_num, button_p->door_id);
        return RETURN_FAILURE;
    }

    // Registering the lines to generate events on falling edge. This is
    // the way that button indicates when it is pressed.
    ret = gpiod_line_request_falling_edge_events(button_p->b_line, CONSUMER);
    if (ret < 0) {
        sd_journal_print(LOG_ALERT, "Failing to request event notification for Button of Door: %d\n",
                         button_p->door_id);
        return RETURN_FAILURE;
    }
    return ret;
}




// The following is the thread which detects when the button is pressed and send this
// event with the door id to the python process using the the posix message queue.
// There is one thread of this for each button.
void *run_button (void *arg_p){
    button_t *button_p = (button_t *) arg_p;
    char q_msg [50];
    int ret;

    enable_button(button_p);

    while (!exit_flag) {
        // Waiting "event_wait_time" for falling edge events in the line
        ret = gpiod_line_event_wait(button_p->b_line, button_p->event_wait_time_p);

        switch (ret) {

            // ret == 1 means an event happened before timout (event_wait_time)
            case 1:
                // Clean the event reading it. If we do not do that, the next call
                // to gpiod_line_event_wait will trigger again (dont remember)
                ret = gpiod_line_event_read(button_p->b_line, &button_p->event);
                // Release the line to avoid more events caused by bounce.
                gpiod_line_release(button_p->b_line);
                // Sleep until bounce finished
                usleep(BOUNCE_TIME);
                // Enable the line again
                enable_button(button_p);
                // Get the value of the line after bounce finished
                ret = gpiod_line_get_value(button_p->b_line);

                // If the value is BUTTON_PRESSED means that the button was really pressed.
                if (BUTTON_PRESSED == ret) {
                    sd_journal_print(LOG_NOTICE, "Button of Door: %d pressed\n", button_p->door_id);
                    // Creating the string that is going to be sent to the message queue.
                    sprintf(q_msg, "%d;0;button=1", button_p->door_id);
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
                // If the value is not BUTTON_PRESSED means that noise came to the line.
                else
                    sd_journal_print(LOG_INFO, "Noise in Button of Door: %d\n", button_p->door_id);
                break;

            // ret == 0 means "event_wait_time" happened and there wasn't any event. In this case
            // nothing is done, and "exit_flag" is checked again at the begining of while loop
            case 0:
                sd_journal_print(LOG_DEBUG, "Thread of Button of Door: %d checking for exit.\n", button_p->door_id);
                break;

            // This would be an unknown error.
            default:
                sd_journal_print(LOG_WARNING, "Unknown error on thread of Button of Door: %d\n", button_p->door_id);
        }

    }

    // When finsih_handler ask to finish setting "exit_flag", before
    // finishing, the line used by the button is released.
    sd_journal_print(LOG_NOTICE, "Thread of Button of Door: %d releasing GPIO: %d.\n", button_p->door_id, button_p->gpio_num);
    gpiod_line_release(button_p->b_line);
    sd_journal_print(LOG_NOTICE, "Thread of Button of Door: %d finished.", button_p->door_id);
}
