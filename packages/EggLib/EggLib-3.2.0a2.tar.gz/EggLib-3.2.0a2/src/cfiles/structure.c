#include <stdlib.h>
#include "structure.h"

void clear_clu(egglib_struct_clu);
void clear_pop(egglib_struct_pop);
void clear_idv(egglib_struct_idv);

egglib_struct * egglib_struct_alloc() {
    egglib_struct * s = malloc(sizeof(egglib_struct));
    if (!s) return s;
    s->nclust = 0;
    s->ploidy = 0;
}

void egglib_struct_free(egglib_struct * s) {
    if (s) {
        if (s->clust) {
            for (unsigned int i=0; i<s->nclust; i++) clear_clu(s->clust[i]);
            free(s->clust);  
        }
        free(s);
    }
}

void clear_clu(egglib_struct_clu clu) {
    if (clu.pop) {
        for (unsigned int i=0; i<clu.npop; i++) clear_pop(clu.pop[i]);
        free(clu.pop);
    }
}

void clear_pop(egglib_struct_pop pop) {
    if (pop.idv) {
        for (unsigned int i=0; i<pop.nidv; i++) clear_idv(pop.idv[i]);
        free(pop.idv);
    }
}

void clear_idv(egglib_struct_idv idv) {
    if (idv.samples) free(idv.samples);
}

void egglib_struct_reset(egglib_struct * s) {
    s->nclust = 0;
    s->ploidy = 0;
}
