#ifndef LIBIOIFACE_H
#define LIBIOIFACE_H
#include <mqueue.h>
#include <gpiod.h>
#include <button.h>
#include <state_snsr.h>
#include <reader.h>
#define RETURN_FAILURE -1
#define RETURN_SUCCESS 0
#define OUTPUT 0
#define INPUT 1
#define NO_FINISH 0
#define FINISH 1
#define BOUNCE_TIME 200000
#define QUEUE_NAME "/ioiface_queue"
#define MAC "86:03:24:b9:a6:b7"
#define MAC_STR_LEN 18 //MAC=12 chars, ":"=5 chars and "\0" char
#define SYS_FILE_MAC "/sys/class/net/eth0/address"
#define CHIP_NAME "gpiochip0"
#define CONSUMER "consumer_name"


extern int exit_flag;
extern mqd_t mq;
extern pthread_mutex_t mq_mutex;


// function prototypes
void finish_handler(int sig_num);

int init_perif(int argc, char *argv[], struct gpiod_chip *chip_p,
               struct timespec *event_wait_time_p, button_t buttons_a[],
               state_snsr_t state_snsrs_a[], reader_t readers_a[]);

int get_number_of(int argc, char *argv[], const char *str);

#endif
