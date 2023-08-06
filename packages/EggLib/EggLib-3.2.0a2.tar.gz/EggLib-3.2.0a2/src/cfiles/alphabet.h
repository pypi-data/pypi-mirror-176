#ifndef EGGLIB_CLIB_ALPHABET_H
#define EGGLIB_CLIB_ALPHABET_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>

struct egglib_alphabet {
    int type; /** type give bitwise information:
                *
                * 1st bit  (1): is int
                * 2nd bit  (2): is cs char
                * 3rd bit  (4): is ci char
                * 4th bit  (8): is cs string
                * 5th bit (16): is ci string
                * 6th bit (32): is custom
                * 7th bit (64): is range
                *
                *       int alphabet: 0b0000001 = 1
                *   ci char alphabet: 0b0000010 = 2
                *   cs char alphabet: 0b0000100 = 4
                * ci string alphabet: 0b0001000 = 8
                * cs string alphabet: 0b0010000 = 16
                *    custom alphabet: 0b0100000 = 32
                *     range alphabet: 0b1000000 = 64
                *
                *       char alphabet: flag&6!=0
                *     string alphabet: flag&24!=0
                *    string or custom: flag&56!=0
                * cs string or custom: flag&48!=0
                **/

    unsigned int nV; ///< number of valid alleles
    unsigned int nM; ///< number of missing alleles
    PyObject ** valid;
    PyObject ** missing;
}

#endif
