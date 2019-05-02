#include <stdio.h>
#include <stdint.h>
#include "BigInt.h"

int main() {
    // BigInt *a = big_create_fromhexstr("0x1234567890");
    // BigInt *b = big_create_fromhexstr("0x1234");
    BigInt *a = big_create_fromll(100);
    BigInt *b = big_create_fromll(300);
    BigInt *c = big_create_fromll(100000007ll);
    big_output(big_powmod(a,b,c));
    return 0;
}
