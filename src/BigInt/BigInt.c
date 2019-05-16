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

extern BigInt *big_oppo(const BigInt *a) {
    BigInt *c = (BigInt *)calloc(1, sizeof(BigInt));
    memcpy(c, a, sizeof(BigInt));
    c->sig = -a->sig;
    return c;
}

extern int big_compare(const BigInt *a, const BigInt *b) {
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

extern BigInt *big_add(const BigInt *a, const BigInt *b) {
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
    int flag = 0;
    for (i = 0; i < c->len; i++) {
        if (flag) c->num[i]++;
        int next_flag = 0;
        if (b->num[i] > 0 && c->num[i] <= a->num[i])
            next_flag = 1;
        flag = next_flag;
    }
    if (c->num[c->len - 1] < a->num[c->len - 1]) {
        if (c->len < MAXLEN) c->len++;
        else {
            puts("Error: big_add -- op1 & op2 are too large");
            big_output(a);
            big_output(b);
            return NULL;
        }
    }
    return c;
}

extern BigInt *big_sub(const BigInt *a, const BigInt *b) {
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
    int flag = 0;
    for (i = 0; i < c->len; i++) {
        if (flag) c->num[i]--;
        int next_flag = 0;
        if (b->num[i] > 0 && c->num[i] >= a->num[i])
            next_flag = 1;
        flag = next_flag;
    }
    while (!c->num[c->len - 1] && c->len > 1) c->len--;
    return c;
}

static int temp_c[MAXLEN];

extern BigInt *big_mul(const BigInt *a, const BigInt *b) {
    BigInt *c = (BigInt *)calloc(1, sizeof(BigInt));
    int i, j;
    c->len = a->len + b->len - 1;
    c->sig = a->sig * b->sig;
    memset(temp_c, 0, sizeof(temp_c));
    for (i = 0; i < a->len; i++)
        for (j = 0; j < b->len; j++)
            if (i + j < MAXLEN)
                temp_c[i + j] += a->num[i] * b->num[j];
            else {
                puts("Error: big_mul -- op1 & op2 are too large");
                big_output(a);
                big_output(b);
                return NULL;
            }
    for (i = 0; i < c->len; i++) {
        temp_c[i + 1] += temp_c[i] >> 8;
        temp_c[i] &= 0xff;
    }
    while (temp_c[c->len]) c->len++;
    for (i = 0; i < c->len; i++)
        c->num[i] = (uint8_t)temp_c[i];
    return c;
}

static uint16_t temp[MAXLEN + 1];
static int temp_len;

static uint8_t big_div_tosmall(BigInt *a, const BigInt *b, int k) {
    uint8_t *aa = a->num + k;
    uint8_t aa_len = a->len - k;
    int l = 0, r = 0x100;
    while (l < r - 1) {
        int mid = (l + r) / 2;
        memset(temp, 0, sizeof(temp));
        int i;
        for (i = 0; i < b->len; i++)
            temp[i] = b->num[i] * mid;
        for (i = 0; i < b->len; i++) {
            temp[i + 1] += temp[i] >> 8;
            temp[i] &= 0xff;
        }
        temp_len = temp[b->len] ? b->len + 1 : b->len;
        if (temp_len > aa_len) r = mid;
        else if (temp_len < aa_len) l = mid;
        else {
            for (i = temp_len - 1; i >= 0; i--)
                if (temp[i] != aa[i])
                    break;
            if (i < 0) l = mid;
            else if (temp[i] < aa[i]) l = mid;
            else r = mid;
        }
    }
    memset(temp, 0, sizeof(temp));
    int i;
    for (i = 0; i < b->len; i++)
        temp[i] = b->num[i] * l;
    for (i = 0; i < b->len; i++) {
        temp[i + 1] += temp[i] >> 8;
        temp[i] &= 0xff;
    }
    temp_len = temp[b->len] ? b->len + 1 : b->len;

#ifdef DEBUG
    big_output(a);
    printf("+0x");
    int j;
    for (j = aa_len - 1; j >= 0; j--)
        printf("%02hx", temp[j]);
    putchar('\n');
#endif

    int flag = 0;
    for (i = 0; i < aa_len; i++) {
        if (flag) aa[i]--;
        int next_flag = 0;
        if ((flag && aa[i] == (uint8_t)0xff) || aa[i] < (uint8_t)temp[i]) 
            next_flag = 1;
        flag = next_flag;
        aa[i] -= (uint8_t)temp[i];
    }
    while (!a->num[a->len - 1] && a->len > 1) a->len--;

#ifdef DEBUG
    printf("%d %d\n", k, l);
    big_output(a);
    putchar('\n');
#endif

    return l;
}

extern BigInt *big_div(const BigInt *a, const BigInt *b, BigInt *r) {
    if (a->sig < 0 || b->sig < 0) {
        puts("Error: big_div -- op1 & op2 should be non-negative");
        big_output(a);
        big_output(b);
        return NULL;
    } else if (b->len == 1 && b->num[0] == 0) {
        puts("Error: big_div -- op2 should not be ZERO");
        big_output(b);
        return NULL;
    }
    if (big_compare(a, b) < 0) {
        memcpy(r, a, sizeof(BigInt));
        return big_create_fromll(0);
    }
    BigInt *c = (BigInt *)calloc(1, sizeof(BigInt));
    BigInt *temp_r = (BigInt *)calloc(1, sizeof(BigInt));
    memcpy(temp_r, a, sizeof(BigInt));
    c->len = a->len - b->len + 1;
    c->sig = 1;
    int i;
    for (i = c->len - 1; i >= 0; i--) {
        uint8_t q = big_div_tosmall(temp_r, b, i);
        c->num[i] = q;
    }
    memcpy(r, temp_r, sizeof(BigInt));
    big_destroy(temp_r);
    while (!c->num[c->len - 1]) c->len--;
    return c;
}

extern BigInt *big_mod(const BigInt *a, const BigInt *b) {
    if (a->sig < 0 || b->sig < 0) {
        puts("Error: big_mod -- op1 & op2 should be non-negative");
        big_output(a);
        big_output(b);
        return NULL;
    } else if (b->len == 1 && b->num[0] == 0) {
        puts("Error: big_mod -- op2 should not be ZERO");
        big_output(b);
        return NULL;
    }
    BigInt *c = (BigInt *)calloc(1, sizeof(BigInt));
    big_div(a, b, c);
    return c;
}

extern BigInt *big_pow(const BigInt *a, const BigInt *b) {
    BigInt *x = (BigInt *)malloc(sizeof(BigInt));
    BigInt *res = big_create_fromll(1ll);
    memcpy(x, a, sizeof(BigInt));
    int i, j;
    for (i = 0; i < b->len; i++) {
        uint8_t now = b->num[i];
        for (j = 0; j < 8; j++) {
            if (now & 1) {
                now &= 0xfe;
                BigInt *passed = res;
                res = big_mul(passed, x);
                big_destroy(passed);
            }
            now >>= 1;
            BigInt *passed = x;
            x = big_mul(passed, passed);
            big_destroy(passed);
        }
    }
    big_destroy(x);
    return res;
}

extern BigInt *big_powmod(const BigInt *a, const BigInt *b, const BigInt *m) {
    BigInt *x = (BigInt *)malloc(sizeof(BigInt));
    BigInt *res = big_create_fromll(1ll);
    memcpy(x, a, sizeof(BigInt));
    int i, j;
    for (i = 0; i < b->len; i++) {
        uint8_t now = b->num[i];
        for (j = 0; j < 8; j++) {
            if (now & 1) {
                now &= 0xfe;
                BigInt *passed = res;
                res = big_mul(passed, x);
                big_destroy(passed);
                passed = res;
                res = big_mod(passed, m);
                big_destroy(passed);
                //printf("j=%d: res=", j);
                //big_output(res);
            }
            now >>= 1;
            BigInt *passed = x;
            x = big_mul(passed, passed);
            big_destroy(passed);
            passed = x;
            x = big_mod(passed, m);
            big_destroy(passed);
            //printf("i=%d: x=", i);
            //big_output(x);
        }
    }
    big_destroy(x);
    return res;

}

extern void big_output(const BigInt *a) {
    //printf("%d ", a->len);
    if (a->sig == -1) putchar('-');
    else if (a->sig == 1) putchar('+');
    int i = 0;
    printf("0x");
    for (i = a->len - 1; i >= 0; i--)
        printf("%02hx", a->num[i]);
    putchar('\n');
}
