#include <python3.6/Python.h>
#include "aes.h"
#include <stdint.h>
#define my_parse_arg(x) PyArg_ParseTuple(args, "iiiiiiiiiiiiiiii", x + 0, x + 1, x + 2, x + 3, x + 4, x + 5, x + 6, x + 7, x + 8, x + 9, x + 10, x + 11, x + 12, x + 13, x + 14, x + 15)
#define my_build_value(x) Py_BuildValue("(iiiiiiiiiiiiiiii)", x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11], x[12], x[13], x[14], x[15])

static aes a = NULL;

static PyObject *wrapper_aes_create(PyObject *self, PyObject *args) {
    if (a) 
	aes_delete(a);
    uint8_t key[0x10];
    if (!my_parse_arg(key))
	return NULL;
    a = aes_create(key);
    aes_calc_subkeys(a);
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *wrapper_aes_delete(PyObject *self, PyObject *args) {
    aes_delete(a);
    a = NULL;
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *wrapper_aes_encrypt(PyObject *self, PyObject *args) {
    PyObject *list = PyTuple_GetItem(args, 0);
    if (!list) 
	return NULL;
    uint8_t plain[0x10];
    uint8_t cipher[0x10];
    if (!my_parse_arg(plain))
	return NULL;

    int i;

    for (i = 0; i < 0x10; i++) printf("%x ", a->key[i]);
    putchar('\n');

    for (i = 0; i < 0x10; i++) printf("%x ", plain[i]);
    putchar('\n');

    aes_encrypt(a, plain, cipher);

    for (i = 0; i < 0x10; i++) printf("%x ", cipher[i]);
    putchar('\n');

    return my_build_value(cipher);
}

static PyObject *wrapper_aes_decrypt(PyObject *self, PyObject *args) {
    PyObject *list = PyTuple_GetItem(args, 0);
    if (!list) 
	return NULL;
    uint8_t cipher[0x10];
    uint8_t plain[0x10];
    if (!my_parse_arg(cipher))
	return NULL;
    aes_decrypt(a, cipher, plain);
    return my_build_value(plain);
}

static PyMethodDef methods[] = {
    {"tell_me_the_devil_secret", wrapper_aes_create, METH_VARARGS, "Tell me the devil secret!!! *byte_list -> None"}, 
    {"forget_the_devil_secret", wrapper_aes_delete, METH_VARARGS, "Forget the devil secret!!! None -> None"},
    {"encrypt", wrapper_aes_encrypt, METH_VARARGS, "Encrypt!!! *byte_list -> byte_tuple"},
    {"decrypt", wrapper_aes_decrypt, METH_VARARGS, "Decrypt!!! *byte_list -> byte_tuple"},
    {NULL, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT, "cAES", NULL, -1, methods
};

PyMODINIT_FUNC PyInit_cAES() {
    return PyModule_Create(&module);
}
