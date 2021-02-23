CC=gcc
IDIR=./include
CFLAGS=-I $(IDIR) -lpthread -lrt -lgpiod -lsystemd -lm
OBJ=main.o common.o button.o state_snsr.o reader.o
_DEPS=common.h button.h state_snsr.h reader.h
DEPS=$(patsubst %,$(IDIR)/%,$(_DEPS))

main: $(OBJ)
	        mkdir -p ../bin/
	        $(CC) -o ../bin/ioiface $(OBJ) $(CFLAGS)


%.o: %.c $(DEPS)
	        $(CC) -c -o $@ $< $(CFLAGS)

clean:
	        rm *.o ../bin/ioiface

