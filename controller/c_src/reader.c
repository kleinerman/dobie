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
#include <math.h>
#include <signal.h>
#include <common.h>
#include <reader.h>




int init_reader(reader_t *reader_p,
                struct gpiod_chip *chip,
                unsigned int wiegand_bits,
                unsigned int d0_gpio_num,
                unsigned int d1_gpio_num,
                unsigned int side,
                unsigned int door_id,
                struct timespec *event_wait_time_p){


    sd_journal_print(LOG_NOTICE, "Reader %d of Door: %d type: %d bits, using GPIO: %d for D0 and GPIO: %d for D1\n",
                     side, door_id, wiegand_bits, d0_gpio_num, d1_gpio_num);
    reader_p->chip = chip;
    reader_p->wiegand_bits = wiegand_bits;
    reader_p->gpio_nums[0] = d0_gpio_num;
    reader_p->gpio_nums[1] = d1_gpio_num;
    reader_p->side = side;
    reader_p->door_id = door_id;
    reader_p->event_wait_time_p = event_wait_time_p;
    reader_p->ini_mask_val = (long long int)pow(2, wiegand_bits-1);
    // The above is the initial value of the mask that should
    // be shifted to the right every time a bit come from the reader.
    // When the bit comming is "1", the mask will be ored with the
    // card number which initial valule will be all bits to "0" and
    // then the mask is shifted for the next bit comming.
    // When the bit comming is "0", only the mask will be shifted.
    //
    // Example in 26 bit wiegand reader:
    // ini_mask_val = 2^(26-1) = 2^25 = 33554432 =
    // = 0000000000000000000000000000000000000010000000000000000000000000
}




int enable_reader(reader_t *reader_p) {
    int ret = RETURN_SUCCESS;

    // Getting two GPIO lines, one for Data 0 and other one for Data 1.
    ret = gpiod_chip_get_lines(reader_p->chip, reader_p->gpio_nums,
                               sizeof(reader_p->gpio_nums)/sizeof(reader_p->gpio_nums[0]),
                               &(reader_p->r_lines));
    if (ret < 0) {
        sd_journal_print(LOG_ALERT, "Error getting lines of GPIOs: %d, %d for Reader of Door: %d\n",
                         reader_p->gpio_nums[0], reader_p->gpio_nums[1], reader_p->door_id);
        return RETURN_FAILURE;
    }

    // Registering both lines to generate events on falling edge. This is the way
    // that readers send bits on Data 0 and Data 1.
    ret = gpiod_line_request_bulk_falling_edge_events(&(reader_p->r_lines), CONSUMER);
    if (ret < 0) {
        sd_journal_print(LOG_ALERT, "Failing to request event notification for Reader: %d of Door: %d\n",
                         reader_p->side, reader_p->door_id);
        return RETURN_FAILURE;
    }
    return ret;
}




// The following is the thread which reads cards on each reader and send
// the card number to the python process using the the posix message queue.
// There is one thread of this for each reader.
void *run_reader (void *arg_p){
    reader_t *reader_p = (reader_t *) arg_p;
    struct gpiod_line_event line_event; // this is used in gpiod_line_event_read()
                                        // to collect the event and clean it for
                                        // the next one.
    char q_msg [50]; //Buffer used to write an send the message to the message queue
    long long int mask, card_number;
    int ret, gpio_num;

    // Enable the line checking if it is not used by another process.
    // If it is used, notify all threads to finish and set the main
    // returned value as FAILURE.
    if (RETURN_FAILURE == enable_reader(reader_p)) {
        exit_flag = FINISH;
        return_exit = RETURN_FAILURE;
    }


    while (!exit_flag) {

        // See the last comment in in init_reader function (above)
        mask = reader_p->ini_mask_val; // Initing mask with initial value
        card_number = 0; // Initing card number all bits to "0"

        while (0 != mask && !exit_flag) { // In every lap check if the mask
                                          // was shifted "wiegand_bits" and
                                          // also if finish_handler asked to finish
            // Waiting for falling edge events in both lines "event_wait_time"
            ret = gpiod_line_event_wait_bulk(&(reader_p->r_lines),
                                             reader_p->event_wait_time_p,
                                             &(reader_p->r_events));

            switch (ret) {

                // ret == 1 means an event happened before timout (event_wait_time)
                case 1:
                    // Getting the line where the bit came.
                    gpio_num = gpiod_line_offset(reader_p->r_events.lines[0]);
                    // Clean the event stored in "r_events.lines[0]". If we do not do
                    // that the next one, blocks or something wrong hapen (dont remember)
                    ret = gpiod_line_event_read(reader_p->r_events.lines[0], &line_event);
                    // If the line is D1, the mask is ored with card number and shifted
                    if (gpio_num == reader_p->gpio_nums[1]) {
                        card_number = card_number | mask;
                    }
                    // If the line is D0, only the mask shifted and nothing is done with card_number
                    mask = mask >> 1;
                    break;

                // ret == 0 means "event_wait_time" happened and there weren't bits comming from the reader
                // If noise enter in any of the lines, to avoid accumulate it, every time "event_wait_time"
                // happen, the mask is reinitiated and the card number is set to "0" again.
                case 0:
                    sd_journal_print(LOG_DEBUG,
                                     "Thread of Reader: %d of Door: %d, cleaning the buffer and checking for exit\n",
                                     reader_p->side, reader_p->door_id);
                    mask = reader_p->ini_mask_val;
                    card_number = 0;
                    break;

                // This would be an unknown error.
                default:
                    sd_journal_print(LOG_WARNING, "Unknown error on thread of Reader: %d of Door: %d\n",
                                     reader_p->side, reader_p->door_id);
            }
        }

        // If the above while loop finished is because the the mask was shifted "wiegand_bits"
        // or because the finsih_handler to finish with "exit_flag". For this reason,
        // before sending the card number to message queue, it is needed to ask if
        // finish_handler asked to finish with "exit_flag"
        if (!exit_flag) {
            // To following will be explained with a wiegand 26 case: A wiegand 26 card number
            // only have 24 bits. The MSB and the LSB bits are just parity bits and should be
            // cleared from the card number. The way that this is done is doing an "AND" operation
            // in the number collected in card_number with the following mask:
            // 0000000000000000000000000000000000000001111111111111111111111110. This mask is got
            // doing: ini_mask_val - 2. After doing the "AND" operation, to have the correct card
            // number, the value should be shifted to the right one position.
            card_number = (card_number & (reader_p->ini_mask_val - 2)) >> 1;
            // Creating the string that is going to be sent to the message queue.
            sprintf(q_msg, "%d;%d;card=%08d", reader_p->door_id, reader_p->side, card_number);
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


    }

    // When finish_handler ask to finish setting "exit_flag", before finishing,
    // both lines used by the reader are released.
    sd_journal_print(LOG_NOTICE,
                     "Thread of Reader: %d of Door: %d releasing GPIO: %d and GPIO: %d\n",
                     reader_p->side, reader_p->door_id, reader_p->gpio_nums[0], reader_p->gpio_nums[1]);
    gpiod_line_release_bulk (&(reader_p->r_lines));
    sd_journal_print(LOG_NOTICE, "Thread of Reader: %d of Door: %d finished.",
                     reader_p->side, reader_p->door_id);

}
