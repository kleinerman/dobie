#ifndef LIBIOIFACE_H
#define LIBIOIFACE_H
#include <mqueue.h>
#include <gpiod.h>
#include <button.h>
#define RETURN_FAILURE -1
#define RETURN_SUCCESS 0
#define BOUNCE_TIME 200000
#define QUEUE_NAME "/ioiface_queue"
#define MAC "<MAC_ADDRESS>"
#define MAC_STR_LEN 18
#define SYS_FILE_MAC "/sys/class/net/<WIRED_IFACE_NAME>/address"
#define CHIP_NAME "gpiochip0"
#define CONSUMER "consumer_name"


extern int exit_flag;
extern mqd_t mq;
extern pthread_mutex_t mq_mutex;


// function prototypes
void finish_handler(int sig_num);
int init_perif(int argc, char **argv, struct gpiod_chip* chip_p, struct timespec* event_wait_time_p, button_t buttons_a[]);
int get_number_of(int argc, char** argv, const char *str);

#endif
