CC=gcc
IDIR=./include
CFLAGS=-I $(IDIR) -lpthread -lrt -lgpiod -lsystemd
OBJ=main.o common.o button.o state_snsr.o
_DEPS=common.h button.h state_snsr.h
DEPS=$(patsubst %,$(IDIR)/%,$(_DEPS))

main: $(OBJ)
	        mkdir -p ../bin/
	        $(CC) -o ../bin/ioiface $(OBJ) $(CFLAGS)


%.o: %.c $(DEPS)
	        $(CC) -c -o $@ $< $(CFLAGS)

clean:
	        rm *.o ../bin/ioiface

