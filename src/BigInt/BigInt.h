#ifndef __qaqmander_BigInt

#define __qaqmander_BigInt

#include <stdint.h>
#define MAXLEN 2048

typedef struct {
    uint8_t num[MAXLEN];
    int len, sig;
} BigInt;

BigInt *big_create_fromhexstr(const char *);

BigInt *big_create_fromll(long long);

void big_destroy(BigInt *);

BigInt *big_oppo(BigInt *);

int big_compare(BigInt *, BigInt *);

BigInt *big_add(BigInt *, BigInt *);

BigInt *big_sub(BigInt *, BigInt *);

BigInt *big_mul(BigInt *, BigInt *);

BigInt *big_div(BigInt *, BigInt *, BigInt *);

void big_output(BigInt *);

#endif
