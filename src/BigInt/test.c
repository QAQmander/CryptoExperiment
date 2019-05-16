#include <stdio.h>
#include <stdint.h>
#include "BigInt.h"

char s[1000];

int main() {
    gets(s);
    BigInt *a = big_create_fromhexstr(s);
    gets(s);
    BigInt *b = big_create_fromhexstr(s);
    gets(s);
    BigInt *c = big_create_fromhexstr(s);
    BigInt *d = big_powmod(a, b, c);
    big_output(d);
    return 0;
}
