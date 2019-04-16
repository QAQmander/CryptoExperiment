#ifndef __qaq_gf242
#define __qaq_gf242

#include <stdint.h>

extern uint8_t gf242_add(uint8_t, uint8_t);

extern uint8_t gf242_sub(uint8_t, uint8_t);

extern uint8_t gf242_mul(uint8_t, uint8_t);

extern uint8_t gf242_inv(uint8_t);

extern uint8_t gf242_create(uint8_t);

extern uint8_t gf242_return(uint8_t);

#endif
