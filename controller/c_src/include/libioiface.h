#ifndef LIBIOIFACE_H
#define LIBIOIFACE_H
#include <mqueue.h>
#define IN 1
#define OUT 0
#define LOW "low"
#define HIGH "high"
#define NONE 0
#define FALLING 1
#define RISING 2
#define BOTH 3

// pssg gpio map
typedef struct {
    int id;                     // pssg identification
    int i0In;                   // GPIO for data D0 (reader input side)
    int i1In;                   // GPIO for data D1 (reader input side)
    int o0In;                   // GPIO for data D0 (reader output side)
    int o1In;                   // GPIO for data D1 (reader output side)
    int button;                 // GPIO for open pssg button 1
    int state;                  // GPIO for state of the pssg (output)
    int buzzer;			// GPIO for buzzer of the pssg (output)
    int release;		// GPIO for release of the pssg (output)
} pssg_t;

struct read_card_args {
    int pssg_id;
    int d0;                     // GPIO for D0
    int d1;                     // GPIO for D1
    char side;                  // Door side: in / out
    mqd_t mq;                   // message queue descriptor
};

struct buttons_args {
    int number_of_pssgs;
    int number_of_buttons;
    pssg_t *pssg;
    mqd_t mq;
};

struct state_args {
    int number_of_pssgs;
    int number_of_states;
    pssg_t *pssg;
    mqd_t mq;
};


// function prototypes
void sigHandler(int signo);
int export_gpio(unsigned int gpio);
int unexport_gpio(unsigned int gpio);
int gpio_set_direction(unsigned int gpio, unsigned int direction);
int gpio_set_edge(unsigned int gpio, unsigned int edge);
int set_gpio_pins (pssg_t *pssg, int number_of_pssgs);
int unset_gpio_pins (pssg_t *pssg, int number_of_pssgs);
int parser(int argc, char **argv, pssg_t *pssg);
int get_number_of(int argc, char** argv, const char *str);
void *read_card (void *args);
int start_readers(int number_of_pssgs, int number_of_readers, pssg_t *pssg, pthread_t *r_thread , mqd_t mq);
void *buttons (void *b_args);
void *state (void *s_args);

#endif
