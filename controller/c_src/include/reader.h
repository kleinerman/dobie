#ifndef READER_H
#define READER_H
#include <common.h>
#include <pthread.h>
#include <mqueue.h>
#include <gpiod.h>

// reader type
typedef struct {

    unsigned int door_id;
    unsigned int wiegand_bits;             // number of weignad bits
    long long int ini_mask_val;
    unsigned int gpio_nums[2];             // gpio_nums[0] = data 0, gpio_nums[1] = data 1
    unsigned int side;                     // 0 = output reader, 1 = input reader
    struct gpiod_chip *chip;               // Name of the chip
    struct gpiod_line_bulk r_lines;        // Bulk of lines
    struct gpiod_line_bulk r_events;       // Bulk of events
    struct timespec *event_wait_time_p;    //Time to wait
    pthread_t r_thread;
} reader_t;


int init_reader(reader_t *reader_p,
                struct gpiod_chip *chip,
                unsigned int wiegand_bits,
                unsigned int d0_gpio_num,
                unsigned int d1_gpio_num,
                unsigned int side,
                unsigned int door_id,
                struct timespec *event_wait_time_p);

int enable_reader(reader_t *reader_p);

void *run_reader (void *arg_p);
#endif
