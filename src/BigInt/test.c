#include <stdio.h>
#include <stdint.h>
#include "BigInt.h"

int main() {
    BigInt *a = big_create_fromhexstr("0xdeadbeef1234567890");
    BigInt *b = big_create_fromhexstr("0xcafebabe");
    BigInt *r = big_create_fromll(0);
    BigInt *q = big_div(a, b, r);
    big_output(a);
    big_output(b);
    big_output(q);
    big_output(r);
    return 0;
}
