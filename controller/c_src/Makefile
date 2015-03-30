CC=gcc
IDIR=./include
CFLAGS=-I $(IDIR) -pthread -lrt
OBJ=main.o access.o
_DEPS=access.h
DEPS=$(patsubst %,$(IDIR)/%,$(_DEPS))

main: $(OBJ)
	        $(CC) -o ioiface $(OBJ) $(CFLAGS)


%.o: %.c $(DEPS)
	        $(CC) -c -o $@ $< $(CFLAGS)

clean:
	        rm *.o ioiface

