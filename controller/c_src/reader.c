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
#include <reader.h>


int init_reader(reader_t * reader_p, 
                struct gpiod_chip *chip, 
                unsigned int d0_gpio_num, 
				unsigned int d1_gpio_num,
				unsigned int door_id,
				struct timespec *event_wait_time_p){


	sd_journal_print(LOG_NOTICE, "Reader of door: %d using GPIO: %d for D0 and GPIO: %d for D1\n",
	                 door_id, d0_gpio_num, d1_gpio_num);
	reader_p->chip = chip;
	reader_p->gpio_nums[0] = d0_gpio_num;
	reader_p->gpio_nums[1] = d1_gpio_num;
	reader_p->door_id = door_id;
	reader_p->event_wait_time_p = event_wait_time_p;

    
}





int enable_reader(reader_t * reader_p) {
	int ret = 0;
	ret = gpiod_chip_get_lines(reader_p->chip, reader_p->gpio_nums,
	                           sizeof(reader_p->gpio_nums)/sizeof(reader_p->gpio_nums[0]),
							   &(reader_p->r_lines));
	if (ret < 0) {
		sd_journal_print(LOG_ALERT, "Error getting lines of GPIOs: %d, %d for reader of door: %d\n", 
		                 reader_p->gpio_nums[0], reader_p->gpio_nums[1], reader_p->door_id);
		return -1;
    }

	ret = gpiod_line_request_bulk_falling_edge_events(&(reader_p->r_lines), CONSUMER);
	if (ret < 0) {
		sd_journal_print(LOG_ALERT, "Failing to request event notification for reader of door: %d\n",
		                 reader_p->door_id);
		return -1;
    }
	return ret;
}








void *run_reader (void *arg_p){
	int ret, gpio_num;
	reader_t *reader_p = (reader_t*) arg_p;
	struct gpiod_line_event line_event;
    char q_msg [50];
	enable_reader(reader_p);
	

	while ( !exit_flag ) {
		
		ret = gpiod_line_event_wait_bulk(&(reader_p->r_lines),
		                                 reader_p->event_wait_time_p,
										 &(reader_p->r_events));

		switch (ret) {
			case 1:
			    gpio_num = gpiod_line_offset(reader_p->r_events.lines[0]);
				printf("Data in GPIO: %d\n", gpio_num);
				ret = gpiod_line_event_read(reader_p->r_events.lines[0], &line_event);
				/*gpiod_line_release(reader_p->b_line);
				usleep(BOUNCE_TIME);
				enable_reader(reader_p);
				ret = gpiod_line_get_value(reader_p->b_line);

				if (READER_PRESSED == ret) {
                    sd_journal_print(LOG_NOTICE, "Reader: %d pressed\n", reader_p->door_id);
					pthread_mutex_lock(&mq_mutex);
                        sprintf(q_msg, "%d;0;reader=1", reader_p->door_id);
						ret = mq_send(mq, q_msg, strlen(q_msg), 1);
						if ( ret == 0 )
							sd_journal_print(LOG_DEBUG, "SUCCESS Sending to queue: %s\n", q_msg);
						else
							sd_journal_print(LOG_ALERT, "ERROR Sending to queue: %s\n", q_msg);
					pthread_mutex_unlock(&mq_mutex);
				} 	
				else
					sd_journal_print(LOG_INFO, "Noise in reader: %d\n", reader_p->door_id);
				*/	
				break;
			case 0:
				sd_journal_print(LOG_DEBUG, "Thread of reader: %d checking for exit\n", reader_p->door_id);
				break;

			default:
				sd_journal_print(LOG_WARNING, "Unknown error on thread of reader: %d\n", reader_p->door_id);
		}

	}
	/*sd_journal_print(LOG_NOTICE, "Thread of reader: %d releasing GPIO: %d\n", reader_p->door_id, reader_p->gpio_num);
    gpiod_line_release(reader_p->b_line);
	sd_journal_print(LOG_NOTICE, "Thread of reader: %d finished.", reader_p->door_id);
    */
}
