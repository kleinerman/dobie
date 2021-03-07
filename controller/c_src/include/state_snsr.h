#ifndef STATE_SNSR_H
#define STATE_SNSR_H
#define STATE_OPEN 0
#define STATE_CLOSE 0
#include <common.h>
#include <button.h>
#include <pthread.h>
#include <mqueue.h>
#include <gpiod.h>

// state_snsr_t type (at the momment is the same as button_t type)
typedef button_t state_snsr_t;

int init_state_snsr(state_snsr_t *state_snsr_p,
                    struct gpiod_chip *chip,
                    unsigned int gpio_num,
                    unsigned int door_id,
                    struct timespec *event_wait_time_p);

int enable_state_snsr(state_snsr_t *state_snsr_p);

void *run_state_snsr (void *arg_p);
#endif
