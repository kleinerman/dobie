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

}





int enable_reader(reader_t *reader_p) {
    int ret = 0;
    ret = gpiod_chip_get_lines(reader_p->chip, reader_p->gpio_nums,
                               sizeof(reader_p->gpio_nums)/sizeof(reader_p->gpio_nums[0]),
                               &(reader_p->r_lines));
    if (ret < 0) {
        sd_journal_print(LOG_ALERT, "Error getting lines of GPIOs: %d, %d for Reader of Door: %d\n",
                         reader_p->gpio_nums[0], reader_p->gpio_nums[1], reader_p->door_id);
        return -1;
    }

    ret = gpiod_line_request_bulk_falling_edge_events(&(reader_p->r_lines), CONSUMER);
    if (ret < 0) {
        sd_journal_print(LOG_ALERT, "Failing to request event notification for Reader of Door: %d\n",
                         reader_p->door_id);
        return -1;
    }
    return ret;
}








void *run_reader (void *arg_p){
    int ret, gpio_num;
    long long int mask, card_number;
    reader_t *reader_p = (reader_t *) arg_p;
    struct gpiod_line_event line_event;
    char q_msg [50];
    enable_reader(reader_p);


    while (!exit_flag) {

        mask = reader_p->ini_mask_val;
        card_number = 0;

        while (0 != mask && !exit_flag){

            ret = gpiod_line_event_wait_bulk(&(reader_p->r_lines),
                                             reader_p->event_wait_time_p,
                                             &(reader_p->r_events));

            switch (ret) {
                case 1:
                    gpio_num = gpiod_line_offset(reader_p->r_events.lines[0]);
                    ret = gpiod_line_event_read(reader_p->r_events.lines[0], &line_event);
                    if (gpio_num == reader_p->gpio_nums[1]) {
                        card_number = card_number | mask;
                    }
                    mask = mask >> 1;
                    break;
                case 0:
                    sd_journal_print(LOG_DEBUG,
                                     "Thread of Reader: %d of Door: %d, cleaning the buffer and checking for exit\n",
                                     reader_p->side, reader_p->door_id);
                    mask = reader_p->ini_mask_val;
                    card_number = 0;
                    break;

                default:
                    sd_journal_print(LOG_WARNING, "Unknown error on thread of Reader: %d of Door: %d\n",
                                     reader_p->side, reader_p->door_id);
            }
        }
        if (!exit_flag) {
            card_number = (card_number & (reader_p->ini_mask_val - 2)) >> 1;
            pthread_mutex_lock(&mq_mutex);
                sprintf(q_msg, "%d;%d;card=%08d", reader_p->door_id, reader_p->side, card_number);
                ret = mq_send(mq, q_msg, strlen(q_msg), 1);
            pthread_mutex_unlock(&mq_mutex);
            if ( ret == 0 )
                sd_journal_print(LOG_INFO, "SUCCESS Sending to queue: %s\n", q_msg);
            else
                sd_journal_print(LOG_ALERT, "ERROR Sending to queue: %s\n", q_msg);
        }


    }
    sd_journal_print(LOG_NOTICE,
                     "Thread of Reader: %d of Door: %d releasing GPIO: %d and GPIO: %d\n",
                     reader_p->side, reader_p->door_id, reader_p->gpio_nums[0], reader_p->gpio_nums[1]);
    gpiod_line_release_bulk (&(reader_p->r_lines));
    sd_journal_print(LOG_NOTICE, "Thread of Reader: %d of Door: %d finished.",
                     reader_p->side, reader_p->door_id);

}
