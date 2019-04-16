#include "aes.h"
#include "gf242.h"
#include <stdlib.h>
#include <string.h>

static void subkey_add(uint8_t *input, uint8_t *subkey) {
    int i;
    for (i = 0; i < 0x10; i++) {
        input[i] ^= subkey[i];
    }
}

static const int8_t row_shift_table[] = {
    0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11
};

static const int8_t row_shift_inv_table[] = {
    0, 13, 10, 7, 4, 1, 14, 11, 8, 5, 2, 15, 12, 9, 6, 3
};

static void row_shift(uint8_t *input, int reverse) {
    uint8_t *temp = (uint8_t *)malloc(0x10);
    memcpy(temp, input, 0x10);
    const int8_t *table = reverse ? row_shift_inv_table 
				  : row_shift_table;
    int i;
    for (i = 0; i < 0x10; i++) {
	input[i] = temp[(int)table[i]];
    }
    free(temp);
}

static const uint8_t column_mix_table[][4] = {
    {0x64, 0x65, 0x01, 0x01},
    {0x01, 0x64, 0x65, 0x01},
    {0x01, 0x01, 0x64, 0x65},
    {0x65, 0x01, 0x01, 0x64}
};

static const uint8_t column_mix_inv_table[][4] = {
    {0x67, 0xbc, 0x02, 0xd8}, 
    {0xd8, 0x67, 0xbc, 0x02},
    {0x02, 0xd8, 0x67, 0xbc},
    {0xbc, 0x02, 0xd8, 0x67}
};

static void column_mix(uint8_t *input, int reverse) {
    const uint8_t (*table)[4] = reverse ? column_mix_inv_table
	                                : column_mix_table;
    uint8_t (*temp)[4] = (uint8_t (*)[4])malloc(4 * 4);
    memcpy(temp, input, 0x10);
    memset(input, 0, 0x10);
    int i, j, k;
    for (i = 0; i < 4; i++)
	for (j = 0; j < 4; j++) {
	    uint8_t ij = 0;
            for (k = 0; k < 4; k++)
		ij = gf242_add(ij, gf242_mul(table[j][k], temp[i][k]));
	    input[4 * i + j] = ij;
	}
    free(temp);
}

static const uint8_t s_box_substitute_table[] = {
    0xb8, 0x54, 0xf2, 0x09, 0x3c, 0xe2, 0x37, 0x01
};

static const uint8_t s_box_substitute_inv_table[] = {
    0x47, 0xab, 0xf2, 0x24, 0x11, 0xcf, 0x1a, 0x01
};

static const uint8_t s_box_vector = 0x87;

static const uint8_t s_box_inv_vector = 0xdb;

static uint8_t s_box_substitute(uint8_t x) {
    uint8_t temp = x;
    temp = gf242_inv(temp);
    int i;
    uint8_t res = 0;
    for (i = 0; i < 8; i++) {
        res <<= 1;
        uint8_t now = temp & s_box_substitute_table[i];
        while (now) {
    	if (now & 1) res ^= 1;
    	now >>= 1;
        }
    }
    res ^= s_box_vector;
    return res;
}

static void byte_substitute(uint8_t *input, int reverse) {
    const uint8_t *table = reverse ? s_box_substitute_inv_table 
	                     : s_box_substitute_table;
    const uint8_t vector = reverse ? s_box_inv_vector
	                           : s_box_vector;
    int i;
    for (i = 0; i < 0x10; i++) {
        uint8_t temp = input[i];
        if (!reverse) 
            temp = gf242_inv(temp);
        int j;
        uint8_t res = 0;
        for (j = 0; j < 8; j++) {
            res <<= 1;
            uint8_t now = temp & table[j];
            while (now) {
        	if (now & 1) res ^= 1;
        	now >>= 1;
            }
        }
        res ^= vector;
        if (reverse)
            res = gf242_inv(res);
        input[i] = res;
    }
}

extern aes aes_create(uint8_t *key) {
    aes a = (aes)malloc(sizeof(struct aes));
    memcpy(a, key, 0x10);
    return a;
}

extern void aes_delete(aes a) {
    free(a);
}

static uint8_t rc[] = {
    0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36
};

extern void aes_calc_subkeys(aes a) {
    uint8_t *key = a->key;
    int i, j;
    for (i = 0; i < 0x10; i++) 
        key[i] = gf242_create(key[i]);
    for (i = 0; i < 10; i++) {
        int base = (i + 1) << 4;
        int former = base - 4;
        key[base + 0] = s_box_substitute(key[former + 1]);
        key[base + 1] = s_box_substitute(key[former + 2]);
        key[base + 2] = s_box_substitute(key[former + 3]);
        key[base + 3] = s_box_substitute(key[former + 0]);
        key[base + 0] ^= gf242_create(rc[i]);
        former = i << 4;
        for (j = 0; j < 4; j++)
            key[base + j] ^= key[former + j];
        for (j = 4; j < 0x10; j++) {
            key[base + j] = key[base + j - 4] ^ key[former + j];
        }
    }
    uint8_t *key_inv = a->key_inv;
    for (i = 0; i < 11; i++) {
        memcpy(key_inv + (i << 4), key + ((10 - i) << 4), 0x10);
    }
    for (i = 1; i < 10; i++) {
        column_mix(key_inv + (i << 4), 1);
    }
}

static void do_something(uint8_t *input, uint8_t *key, int reverse) {
    int i;
    subkey_add(input, key + (0 << 4));
    for (i = 1; i < 10; i++) {
        byte_substitute(input, reverse);
        row_shift(input, reverse);
        column_mix(input, reverse);
        subkey_add(input, key + (i << 4));
    }
    byte_substitute(input, reverse);
    row_shift(input, reverse);
    subkey_add(input, key + (10 << 4));
}

extern void aes_encrypt(aes a, uint8_t *plain, uint8_t *cipher) {
    int i;
    for (i = 0; i < 0x10; i++)
        cipher[i] = gf242_create(plain[i]);
    do_something(cipher, a->key, 0);
    for (i = 0; i < 0x10; i++)
        cipher[i] = gf242_return(cipher[i]);
}

extern void aes_decrypt(aes a, uint8_t *cipher, uint8_t *plain) {
    int i;
    for (i = 0; i < 0x10; i++)
        plain[i] = gf242_create(cipher[i]);
    do_something(plain, a->key_inv, 1);
    for (i = 0; i < 0x10; i++)
        plain[i] = gf242_return(plain[i]);
}

