CC=gcc
IDIR=./include
CFLAGS=-I $(IDIR) -pthread -lrt
OBJ=main.o libioiface.o
_DEPS=libioiface.h
DEPS=$(patsubst %,$(IDIR)/%,$(_DEPS))

main: $(OBJ)
	        $(CC) -o ../bin/ioiface $(OBJ) $(CFLAGS)


%.o: %.c $(DEPS)
	        $(CC) -c -o $@ $< $(CFLAGS)

clean:
	        rm *.o ioiface

