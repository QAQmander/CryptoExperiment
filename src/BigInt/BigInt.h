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

BigInt *big_oppo(const BigInt *);

int big_compare(const BigInt *, const BigInt *);

BigInt *big_add(const BigInt *, const BigInt *);

BigInt *big_sub(const BigInt *, const BigInt *);

BigInt *big_mul(const BigInt *, const BigInt *);

BigInt *big_div(const BigInt *, const BigInt *, BigInt *);

void big_output(const BigInt *);

#endif
