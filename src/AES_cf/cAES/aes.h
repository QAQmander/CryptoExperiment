
#ifndef __qaq_aes
#define __qaq_aes

#include <stdint.h>

typedef struct aes {
    uint8_t key[16 * 11];
    uint8_t key_inv[16 * 11];
} *aes;

extern aes aes_create(uint8_t *);

extern void aes_delete(aes);

extern void aes_calc_subkeys(aes);

extern void aes_encrypt(aes, uint8_t *, uint8_t *);

extern void aes_decrypt(aes, uint8_t *, uint8_t *);

#endif
