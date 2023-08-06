#ifndef EGGLIB_CLIB_STRUCTURE_H
#define EGGLIB_CLIB_STRUCTURE_H

typedef struct egglib_struct_clu egglib_struct_clu;
typedef struct egglib_struct_pop egglib_struct_pop;
typedef struct egglib_struct_idv egglib_struct_idv;

typedef struct {
    egglib_struct_clu * clust;
    unsigned int ploidy, nclust, cclust;
} egglib_struct;

typedef struct egglib_struct_clu {
    egglib_struct * parent;
    egglib_struct_pop * pop;
    unsigned int npop, cpop;
} egglib_struct_clu;

typedef struct egglib_struct_pop {
    egglib_struct_clu * parent;
    egglib_struct_idv * idv;
    unsigned int nidv, cidv;
} egglib_struct_pop;

typedef struct egglib_struct_idv {
    egglib_struct_pop * parent;
    unsigned int * samples;
} egglib_struct_idv;


egglib_struct * egglib_struct_alloc(); ///< allocate object and initialize (NULL if memory error)
void egglib_struct_free(egglib_struct *); ///< free allocated memory
void egglib_struct_reset(egglib_struct *); ///< reset object

#endif
