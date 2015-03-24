#ifndef ACCESS_H
#define ACCESS_H
#include <mqueue.h>
#define IN 1
#define OUT 0
#define LOW "low"
#define HIGH "high"
#define NONE 0
#define FALLING 1
#define RISING 2
#define BOTH 3

// door gpio map
typedef struct {
    int id;                     // door identification
    int i0;                     // GPIO for data D0 (reader 1)
    int i1;                     // GPIO for data D1 (reader 1)
    int o0;                     // GPIO for data D0 (reader 2)
    int o1;                     // GPIO for data D1 (reader 2)
    int button;                 // GPIO for open door button 1
    int state;                  // GPIO for state of the door (output)
} door_t;

struct read_card_args {
    int door_id;
    int d0;                     // GPIO for D0
    int d1;                     // GPIO for D1
    char side;                  // Door side: in / out
    mqd_t mq;                   // message queue descriptor
};

struct buttons_args {
    int number_of_doors;
    int number_of_buttons;
    door_t *door;
    mqd_t mq;
};


// function prototypes
int export_gpio(unsigned int gpio);
int gpio_set_direction(unsigned int gpio, unsigned int direction);
int gpio_set_edge(unsigned int gpio, unsigned int edge);
int parser(int argc, char **argv, door_t *door);
int get_number_of(int argc, char** argv, const char *str);
void *read_card (void *args);
int start_readers(int number_of_doors, int number_of_readers, door_t *door, pthread_t *thread , mqd_t mq);
void *buttons (void *b_args);

#endif
