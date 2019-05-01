#include <stdio.h>
#include <stdint.h>
#include "BigInt.h"

int main() {
    BigInt *a = big_create_fromll(123456789);
    BigInt *b = big_create_fromll(987654321);
    big_output(big_oppo(a));
    big_output(big_add(a,b));
    big_output(big_sub(a,b));
    big_output(big_mul(a,b));
    return 0;
}
