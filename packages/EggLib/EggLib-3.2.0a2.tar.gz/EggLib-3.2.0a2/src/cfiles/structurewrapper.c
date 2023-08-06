#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"
#include "structure.h"

// STRUCTURE TYPE

typedef struct {
    PyObject_HEAD
    egglib_struct * cstruct;
    unsigned int ni, no, nclust, npop, nidvi, nidvo;
} structure_type;

static PyObject * get_ploidy(PyObject * self, PyObject * Py_UNUSED(ignored)) {
    if (((structure_type *)self)->cstruct->ploidy == 0) Py_RETURN_NONE;
    return PyLong_FromLong(((structure_type *)self)->cstruct->ploidy);
}

// methods
static PyMethodDef Structure_methods[] = {
    {"get_ploidy",  (PyCFunction) get_ploidy, METH_NOARGS, "Get ploidy."},
    {NULL, NULL, 0, NULL}
};

// simple members
static PyMemberDef Structure_members[] = {
    {"no", T_UINT, offsetof(structure_type, no), READONLY, "Number of outgroup samples."},
    {"ni", T_UINT, offsetof(structure_type, ni), READONLY, "Number of ingroup samples."},
    {"num_clust", T_UINT, offsetof(structure_type, nclust), READONLY, "Number of clusters."},
    {"num_pop", T_UINT, offsetof(structure_type, npop), READONLY, "Number of populations."},
    {"num_indiv_ingroup", T_UINT, offsetof(structure_type, nidvi), READONLY, "Number of ingroup individuals."},
    {"num_indiv_outgroup", T_UINT, offsetof(structure_type, nidvo), READONLY, "Number of outgroup individuals."},
    {NULL}
};

static PyGetSetDef Structure_getset[] = {
    {"ploidy",  (getter) get_ploidy, NULL, "Ploidy.", NULL},
    {NULL}
};

// memory managemnt
static PyObject * Structure_new(PyTypeObject * type, PyObject * args, PyObject * kwds) {
    structure_type * self = (structure_type *) type->tp_alloc(type, 0);
    if (!self) return NULL;
    self->cstruct = malloc(sizeof(egglib_struct)); // no need to initialize
    if (!self->cstruct) { Py_TYPE(self)->tp_free((PyObject *) self); return NULL; }
    self->cstruct->clust = NULL;
    self->cstruct->cclust = 0;
    return (PyObject *) self;
}

static int Structure_init(PyObject * self, PyObject * args, PyObject * kwds) {
    egglib_struct_reset(((structure_type *)self)->cstruct);
    return 0;
}

static void Structure_dealloc(PyObject * self) {
    egglib_struct_free(((structure_type *)self)->cstruct);
    Py_TYPE(self)->tp_free((PyObject *) self);
}

// declaration of type
static PyTypeObject Structure_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "_structure.Structure",
    .tp_doc = "Class describing the organisation of samples.",
    .tp_basicsize = sizeof(structure_type),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = Structure_new,
    .tp_init = (initproc) Structure_init,
    .tp_dealloc = (destructor) Structure_dealloc,
    .tp_methods = Structure_methods,
    .tp_members = Structure_members,
    .tp_getset = Structure_getset
};

// MODULE CONFIGURATION

static PyMethodDef structure_methods[] = {
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef structuremodule = {
    PyModuleDef_HEAD_INIT,
    "structure",                          /* name of module */
    "Tools to describe structure",        /* module documentation, may be NULL */
    -1,                                   /* size of per-interpreter state of the module */
    structure_methods
};

PyMODINIT_FUNC PyInit__structure(void) {
    if (PyType_Ready(&Structure_type) < 0) return NULL;
    PyObject * m = PyModule_Create(&structuremodule);
    if (!m) return NULL;

    Py_INCREF(&Structure_type);
    if (PyModule_AddObject(m, "Structure", (PyObject *) &Structure_type) < 0) {
        Py_DECREF(&Structure_type);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
