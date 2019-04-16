#include "gf242.h"

#define GET_LOW(x) ((x) & 0xf)
#define GET_HIGH(x) (((x) & 0xf0) >> 4) 
#define MAKE(h, l) (((h) << 4) | l)

#define gf24_add(x, y) ((x) ^ (y))
#define gf24_sub(x, y) ((x) ^ (y))
#define gf24_inv(x) (gf24_inv_table[x])

#define return_matrix_mul(a, x) \
int i;                          \
uint8_t res = 0;                \
for (i = 0; i < 8; i++) {       \
    res <<= 1;                  \
    uint8_t now = x & a[i];     \
    while (now) {               \
        if (now & 1) res ^= 1;  \
        now >>= 1;              \
    }                           \
}                               \
return res

/*
static uint8_t gf24_add(uint8_t x, uint8_t y) {
    return x ^ y;
}

static uint8_t gf24_sub(uint8_t x, uint8_t y) {
    return x ^ y;
}
*/

static uint8_t gf24_mul(uint8_t x, uint8_t y) {
    uint8_t res = 0;
    while (y) {
        if (y & 1) res ^= x;
        if (res & 0x10) res ^= 0x19;
        y >>= 1;
        x <<= 1;
        if (x & 0x10) x ^= 0x19;
    }
    return res;
}

static const uint8_t gf24_inv_table[] = {
    0x0, 0x1, 0xC, 0x8,
    0x6, 0xF, 0x4, 0xE,
    0x3, 0xD, 0xB, 0xA,
    0x2, 0x9, 0x7, 0x5
};

/*
static uint8_t gf24_inv(uint8_t x) {
    return gf24_inv_table[x];
}
*/

extern uint8_t gf242_add(uint8_t x, uint8_t y) {
    return x ^ y;
}

extern uint8_t gf242_sub(uint8_t x, uint8_t y) {
    return x ^ y;
}

extern uint8_t gf242_mul(uint8_t x, uint8_t y) {
    uint8_t xl = GET_LOW(x);
    uint8_t xh = GET_HIGH(x);
    uint8_t yl = GET_LOW(y);
    uint8_t yh = GET_HIGH(y);
    uint8_t res_l = gf24_mul(xl, yl);
    uint8_t res_m = gf24_add(gf24_mul(xl, yh), gf24_mul(xh, yl));
    uint8_t res_h = gf24_mul(xh, yh);
    res_m = gf24_sub(res_m, res_h);
    res_l = gf24_sub(res_l, gf24_mul(res_h, 0x2));
    return MAKE(res_m, res_l);
}

extern uint8_t gf242_inv(uint8_t x) {
    uint8_t c = GET_LOW(x);
    uint8_t b = GET_HIGH(x);
    uint8_t delta = gf24_add(gf24_add(gf24_mul(b, c), 
		gf24_mul(c, c)), gf24_mul(0x2, gf24_mul(b, b)));
    delta = gf24_inv(delta);
    uint8_t res_l = gf24_mul(delta, gf24_add(b, c));
    uint8_t res_h = gf24_mul(delta, b);
    return MAKE(res_h, res_l);
}

static const uint8_t isomorphic_a[] = {
    0xac, 0xde, 0xd2, 0x7c, 0x8c, 0x92, 0xa4, 0x99
};

extern uint8_t gf242_create(uint8_t x) {
    return_matrix_mul(isomorphic_a, x);
}

static const uint8_t isomorphic_a_inv[] = {
    0x68, 0x24, 0x88, 0xdc, 0x82, 0xe2, 0xb0, 0x37
};

extern uint8_t gf242_return(uint8_t x) {
    return_matrix_mul(isomorphic_a_inv, x);
}

