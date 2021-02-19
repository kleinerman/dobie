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

int init_button(button_t * button_p, 
                struct gpiod_chip *chip, 
                unsigned int gpio_num, 
				unsigned int door_id,
				struct timespec *event_wait_time_p){
    
	sd_journal_print(LOG_NOTICE, "Button of door: %d using GPIO: %d\n",
	                 door_id, gpio_num);
	button_p->chip = chip;
	button_p->gpio_num = gpio_num;
	button_p->door_id = door_id;
	button_p->event_wait_time_p = event_wait_time_p;

    
}





int enable_button(button_t * button_p) {
	int ret = 0;
	button_p->b_line = gpiod_chip_get_line(button_p->chip, button_p->gpio_num);
	if (!button_p->b_line) {
		sd_journal_print(LOG_ALERT, "Error getting line of GPIO: %d for button of door: %d\n", 
		                 button_p->gpio_num, button_p->door_id);
		return -1;
    }

	ret = gpiod_line_request_falling_edge_events(button_p->b_line, CONSUMER);
	if (ret < 0) {
		sd_journal_print(LOG_ALERT, "Failing to request event notification for button of door: %d\n",
		                 button_p->door_id);
		return -1;
    }
	return ret;
}








void *run_button (void *arg_p){
	int ret;
	button_t *button_p = (button_t*) arg_p;
    char q_msg [50];
	enable_button(button_p);
	

	while ( !exit_flag ) {
		
		ret = gpiod_line_event_wait(button_p->b_line, button_p->event_wait_time_p);

		switch (ret) {
			case 1:
				ret = gpiod_line_event_read(button_p->b_line, &button_p->event);
				gpiod_line_release(button_p->b_line);
				usleep(BOUNCE_TIME);
				enable_button(button_p);
				ret = gpiod_line_get_value(button_p->b_line);

				if (BUTTON_PRESSED == ret) {
                    sd_journal_print(LOG_NOTICE, "Button: %d pressed\n", button_p->door_id);
					pthread_mutex_lock(&mq_mutex);
                        sprintf(q_msg, "%d;0;button=1", button_p->door_id);
						ret = mq_send(mq, q_msg, strlen(q_msg), 1);
						if ( ret == 0 )
							sd_journal_print(LOG_DEBUG, "SUCCESS Sending to queue: %s\n", q_msg);
						else
							sd_journal_print(LOG_ALERT, "ERROR Sending to queue: %s\n", q_msg);
					pthread_mutex_unlock(&mq_mutex);
				} 	
				else
					sd_journal_print(LOG_INFO, "Noise in button: %d\n", button_p->door_id);
				break;

			case 0:
				sd_journal_print(LOG_DEBUG, "Thread of button: %d checking for exit\n", button_p->door_id);
				break;

			default:
				sd_journal_print(LOG_WARNING, "Unknown error on thread of button: %d\n", button_p->door_id);
		}

	}
	sd_journal_print(LOG_NOTICE, "Thread of button: %d releasing GPIO: %d\n", button_p->door_id, button_p->gpio_num);
    gpiod_line_release(button_p->b_line);
	sd_journal_print(LOG_NOTICE, "Thread of button: %d finished.", button_p->door_id);

}
