#ifndef BUTTON_H
#define BUTTON_H
#define BUTTON_PRESSED 0
#include <common.h>
#include <pthread.h>
#include <mqueue.h>
#include <gpiod.h>

// button type
typedef struct {

    unsigned int door_id;
    unsigned int gpio_num;               // GPIO number used
    struct gpiod_chip *chip;             // Name of the chip
    struct gpiod_line *b_line;           // Pointer to gpiod line
    struct gpiod_line_event event;       // To read the events
    struct timespec *event_wait_time_p;  //Time to wait events in button
    pthread_t b_thread;
} button_t;


int init_button(button_t *button_p,
                struct gpiod_chip *chip,
                unsigned int gpio_num,
                unsigned int door_id,
                struct timespec *event_wait_time_p);

int enable_button(button_t *button_p);

void *run_button (void *arg_p);
#endif
