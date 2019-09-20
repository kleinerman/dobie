#ifndef LIBIOIFACE_H
#define LIBIOIFACE_H
#define RPi
#include <mqueue.h>
#define IN 1
#define OUT 0
#define LOW "low"
#define HIGH "high"
#define NONE 0
#define FALLING 1
#define RISING 2
#define BOTH 3
#define RETURN_FAILURE -1
#define RETURN_SUCCESS 0
#define UNDEFINED -1
#define EPOLL_WAIT_TIME 2000
#define BOUNCE_TIME 200000
#define QUEUE_NAME "/ioiface_queue"
#define MAC "<MAC_ADDRESS>"
#define MAC_STR_LEN 18
#define SYS_FILE_MAC "/sys/class/net/<WIRED_IFACE_NAME>/address"


// door gpio map
typedef struct {
    int id;                     // door identification
    int i0In;                   // GPIO for data D0 (reader input side)
    int i1In;                   // GPIO for data D1 (reader input side)
    int o0In;                   // GPIO for data D0 (reader output side)
    int o1In;                   // GPIO for data D1 (reader output side)
    int button;                 // GPIO for open door button
    int state;                  // GPIO for state of the door (output)
    int buzzer;			// GPIO for buzzer of the door (output)
    int release;		// GPIO for release of the door (output)
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

struct state_args {
    int number_of_doors;
    int number_of_states;
    door_t *door;
    mqd_t mq;
};


// function prototypes
void sigHandler(int signo);
int export_gpio(unsigned int gpio);
int unexport_gpio(unsigned int gpio);
int gpio_set_direction(unsigned int gpio, unsigned int direction);
int gpio_set_edge(unsigned int gpio, unsigned int edge);
int set_gpio_pins (door_t *door, int number_of_doors);
int unset_gpio_pins (door_t *door, int number_of_doors);
int parser(int argc, char **argv, door_t *door);
int get_number_of(int argc, char** argv, const char *str);
void *read_card (void *args);
int start_readers(int number_of_doors, int number_of_readers, door_t *door, pthread_t *r_thread , mqd_t mq);
void *buttons (void *b_args);
void *state (void *s_args);

#endif
