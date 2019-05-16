
CC=cc
FLAG=-O3 -c -W -Wall

a.out : test.o BigInt.o
	$(CC) -o $@ $^

test.o : test.c BigInt.h
	$(CC) $(FLAG) -o $@ $<

BigInt.o : BigInt.c BigInt.h
	$(CC) $(FLAG) -o $@ $<

.PHONY: clean
clean :
	rm test.o BigInt.o
