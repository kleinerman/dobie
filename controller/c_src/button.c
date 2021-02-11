#include <gpiod.h>
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

int init_button(button_t * button_p, 
                struct gpiod_chip *chip, 
                unsigned int gpio_num, 
				unsigned int door_id,
				struct timespec *event_wait_time_p){
    
	button_p->chip = chip;
	button_p->gpio_num = gpio_num;
	button_p->door_id = door_id;
	button_p->event_wait_time_p = event_wait_time_p;
    
}



int enable_button(button_t * button_p) {
	int ret = 0;
	button_p->b_line = gpiod_chip_get_line(button_p->chip, button_p->gpio_num);
	if (!button_p->b_line) {
		perror("Get line failed\n");
		ret = -1;
	}

	ret = gpiod_line_request_falling_edge_events(button_p->b_line, CONSUMER);
	if (ret < 0) {
		perror("Request event notification failed\n");
		ret = -1;
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
					printf("Button: %d pressed\n", button_p->door_id);
					pthread_mutex_lock(&mq_mutex);
                        sprintf(q_msg, "%d;0;button=1", button_p->door_id);
      					ret = mq_send(mq, q_msg, strlen(q_msg), 1);
						if ( ret == 0 ) printf("Success sending to MQ!!\n");
						else printf("Error sending to MQ!!\n");
					pthread_mutex_unlock(&mq_mutex);
				} 	
				else {
					printf("Noise in: %d\n", button_p->door_id);
				}
				break;

			case 0:
				printf("Button thread: %d checking request to finish.\n", button_p->door_id);
				break;

			default:
				printf("Error in Button: %d.\n", button_p->door_id);
		}

	}
    printf("Finishing button: %d.\n", button_p->door_id);

}
