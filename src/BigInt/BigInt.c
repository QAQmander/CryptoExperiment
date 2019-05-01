#include "BigInt.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static uint8_t single_hex_to_uint(char x) {
    if ('0' <= x && x <= '9')
        return x - '0';
    if ('a' <= x && x <= 'f')
        return x - 'a' + 10;
    if ('A' <= x && x <= 'F')
        return x - 'A' + 10;
    printf("Error: single_hex_to_uint -- unknown hexchar {%c %d}\n", x, x);
    return -1;
}

static uint8_t hex_to_uint(char h, char l) {
    return single_hex_to_uint(h) * 16 + single_hex_to_uint(l);
}

extern BigInt *big_create_fromhexstr(const char *s) {
    BigInt *ret = (BigInt *)calloc(1, sizeof(BigInt));
    ret->sig = (s[0] == '-') ? -1 : 1;
    const char *p = (const char *)strchr(s, 'x');
    p = p ? p + 1 : s;
    while (*p == '0') p++;
    int length = strlen(p);
    if (length > MAXLEN * 2) {
        printf("Error: big_create_fromhexstr -- hexstr is too long {%s}\n", s);
        return NULL;
    }
    int i;
    for (i = 0; i < length - 1; i += 2) {
        char nowh = p[length - i - 2];
        char nowl = p[length - i - 1];
        ret->num[i / 2] = hex_to_uint(nowh, nowl);
    }
    ret->len = (length - 1) / 2 + 1;
    char nowh = (length % 2) ? '0' : p[0];
    char nowl = (length % 2) ? p[0] : p[1];
    ret->num[ret->len - 1] = hex_to_uint(nowh, nowl);
    return ret;
}

extern BigInt *big_create_fromll(long long x) {
    BigInt *ret = (BigInt *)calloc(1, sizeof(BigInt));
    if (x < 0) ret->sig = -1, x = -x;
    else ret->sig = 1;
    while (x) {
        ret->num[ret->len++] = (uint8_t)(x & 0xff);
        x >>= 8;
    }
    return ret;
}

extern void big_destroy(BigInt *a) {
    free(a);
}

extern BigInt *big_oppo(BigInt *a) {
    BigInt *c = (BigInt *)calloc(1, sizeof(BigInt));
    memcpy(c, a, sizeof(BigInt));
    c->sig = -a->sig;
    return c;
}

extern int big_compare(BigInt *a, BigInt *b) {
    if (a->sig > b->sig) return 1;
    if (a->sig < b->sig) return -1;
    int sig = a->sig;
    if (a->len > b->len) return 1 * sig;
    if (a->len < b->len) return -1 * sig;
    int len = a->len;
    int i;
    for (i = len - 1; i >= 0; i--)
        if (a->num[i] < b->num[i])
            return -1 * sig;
        else if (a->num[i] > b->num[i])
            return 1 * sig;
    return 0;
}

extern BigInt *big_add(BigInt *a, BigInt *b) {
    if (a->sig != b->sig) {
        BigInt *b_oppo = big_oppo(b);
        BigInt *res = big_sub(a, b_oppo);
        big_destroy(b_oppo);
        return res;
    }
    BigInt *c = (BigInt *)calloc(1, sizeof(BigInt));
    c->sig = a->sig;
    c->len = (a->len > b->len) ? a->len : b->len;
    int i;
    for (i = 0; i < c->len; i++)
        c->num[i] = a->num[i] + b->num[i];
    for (i = 0; i < c->len - 1; i++)
        if (c->num[i] < a->num[i])
            c->num[i + 1]++;
    if (c->num[c->len - 1] < a->num[c->len - 1]) {
        if (c->len < MAXLEN) c->len++;
        else {
            puts("Error: big_add -- a and b is too large!!");
            big_output(a);
            big_output(b);
            return NULL;
        }
    }
    return c;
}

extern BigInt *big_sub(BigInt *a, BigInt *b) {
    if (a->sig != b->sig) {
        BigInt *b_oppo = big_oppo(b);
        BigInt *res = big_add(a, b_oppo);
        big_destroy(b_oppo);
        return res;
    }
    if (a->sig < 0) {
        BigInt *a_oppo = big_oppo(a);
        BigInt *b_oppo = big_oppo(b);
        BigInt *res = big_sub(b_oppo, a_oppo);
        big_destroy(a_oppo);
        big_destroy(b_oppo);
        return res;
    }
    if (big_compare(a, b) < 0) {
        BigInt *res_oppo = big_sub(b, a);
        BigInt *res = big_oppo(res_oppo);
        big_destroy(res_oppo);
        return res;
    }
    BigInt *c = (BigInt *)calloc(1, sizeof(BigInt));
    c->sig = a->sig;
    c->len = a->len;
    int i;
    for (i = 0; i < c->len; i++)
        c->num[i] = a->num[i] - b->num[i];
    for (i = 0; i < c->len - 1; i++)
        if (c->num[i] > a->num[i])
            c->num[i + 1]--;
    while (!c->num[c->len - 1] && c->len > 1) c->len--;
    return c;
}

static int temp_c[MAXLEN];

extern BigInt *big_mul(BigInt *a, BigInt *b) {
    BigInt *c = (BigInt *)calloc(1, sizeof(BigInt));
    int i, j;
    c->len = a->len + b->len;
    c->sig = a->sig * b->sig;
    memset(temp_c, 0, sizeof(temp_c));
    for (i = 0; i < a->len; i++)
        for (j = 0; j < b->len; j++)
            if (i + j < MAXLEN)
                temp_c[i + j] += a->num[i] * b->num[j];
            else {
                puts("Error: big_mul -- a and b is too large!!");
                big_output(a);
                big_output(b);
                return NULL;
            }
    for (i = 0; i < c->len; i++) {
        temp_c[i + 1] += temp_c[i] >> 8;
        temp_c[i] = temp_c[i] & 0xff;
    }
    for (i = 0; i < c->len; i++)
        c->num[i] = (uint8_t)temp_c[i];
    return c;
}

extern void big_output(BigInt *a) {
    printf("%d ", a->len);
    if (a->sig == -1) putchar('-');
    else if (a->sig == 1) putchar('+');
    int i = 0;
    printf("0x");
    for (i = a->len - 1; i >= 0; i--)
        printf("%02hx", a->num[i]);
    putchar('\n');
}
