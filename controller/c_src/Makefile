CC=gcc
IDIR=./include
CFLAGS=-I $(IDIR) -pthread -lrt -lgpiod
OBJ=main.o common.o button.o
_DEPS=common.h button.h
DEPS=$(patsubst %,$(IDIR)/%,$(_DEPS))

main: $(OBJ)
	        mkdir -p ../bin/
	        $(CC) -o ../bin/ioiface $(OBJ) $(CFLAGS)


%.o: %.c $(DEPS)
	        $(CC) -c -o $@ $< $(CFLAGS)

clean:
	        rm *.o ../bin/ioiface

