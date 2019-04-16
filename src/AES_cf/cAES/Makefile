FLAGS = -O3 -fPIC
CC = cc

cAES.so: cAES.o aes.o gf242.o
	$(CC) -shared -o $@ $^ 

cAES.o: cAES.c aes.h
	$(CC) $(FLAGS) -c -o $@ $<

gf242.o: gf242.c
	$(CC) $(FLAGS) -c -o $@ $< 

aes.o: aes.c gf242.h 
	$(CC) $(FLAGS) -c -o $@ $< 

.PHONY: clean
clean:
	-rm gf242.o aes.o cAES.o
