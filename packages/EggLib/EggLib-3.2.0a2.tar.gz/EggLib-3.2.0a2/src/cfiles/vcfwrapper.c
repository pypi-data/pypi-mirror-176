#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

#include <string.h>
#include "htslib/hts_log.h"
#include "htslib/hts.h"
#include "htslib/vcf.h"

/********************************
    GLOBAL FUNCTION
*********************************/

static PyObject * vcf_index_vcf(PyObject * self, PyObject * args, PyObject * kwargs) {
    const char * s1;
    const char * s2 = NULL;
    static char * kwlist[] = {"fname", "outname", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|s", kwlist, &s1, &s2)) {
        return NULL;
    }
    int min_shift = 14; // 14 is the recommended value for min_shift
    int ret = s2 ? bcf_index_build2(s1, s2, min_shift) : bcf_index_build(s1, min_shift);
    if (ret == 0) Py_RETURN_NONE;
    if (ret == -1) {
        PyErr_SetString(PyExc_ValueError, "Cannot create index: indexing failed");
        return NULL;
    }
    if (ret == -2) {
        PyErr_SetString(PyExc_OSError, "Cannot create index: cannot open file");
        return NULL;
    }
    if (ret == -3) {
        PyErr_SetString(PyExc_ValueError, "Cannot create index: format not indexable");
        return NULL;
    }
    if (ret == -4) {
        PyErr_SetString(PyExc_OSError, "Cannot create index: failed to create and/or save the index");
        return NULL;
    }
    PyErr_SetString(PyExc_ValueError, "Cannot create index: undefined error");
    return NULL;
}

/********************************
    DEFINITION OF PARSER TYPE
*********************************/

static const int NUM_TYPES = 5;
static const int TYPES[] = {VCF_SNP, VCF_MNP, VCF_INDEL, VCF_OTHER, VCF_BND};
static const char * TYPENAMES[] = {"SNP", "MNP", "INDEL", "OTHER", "BND", "OVERLAP"};

static const int NUM_ERRORS = 7;
static const int ERRORS[] = {BCF_ERR_CTG_UNDEF, BCF_ERR_TAG_UNDEF,
    BCF_ERR_NCOLS, BCF_ERR_LIMITS, BCF_ERR_CHAR, BCF_ERR_CTG_INVALID,
    BCF_ERR_TAG_INVALID};
static const char * ERRORNAMES[] = {"ERR_CTG_UNDEF", "ERR_TAG_UNDEF",
    "ERR_NCOLS", "ERR_LIMITS", "ERR_CHAR", "ERR_CTG_INVALID",
    "ERR_TAG_INVALID"};

typedef struct {
    PyObject_HEAD
    htsFile * pfile;
    bcf_hdr_t * hdr;
    int num_samples;
    bcf1_t * record;
    int status; // 1 if a line has been read
    int types; // variant type flag (is status)
    PyObject ** type_strings; // strings representing names of variant types
    PyObject ** error_strings; // strings representing names of non fatal-errors
    hts_idx_t * index; // NULL if index cannot be loaded
    char has_index; // 1 if index is not NULL

    // internal usage memory (to write info/format parsing results)
    int32_t * p_int;
    int n_int;
    float * p_float;
    int n_float;
    char * p_str;
    int n_str;

    int32_t * gt_p; // for GT field
    int gt_n;
    int gt_num; // value of given by last call to get_genotypes (reset to 0 at each read/goto)
} VCF_object;

/******************************
    CREATION/DELETION METHODS
*******************************/

// DEL METHOD
static void VCF_dealloc(VCF_object * self) {
    if (self->hdr) bcf_hdr_destroy(self->hdr);
    if (self->pfile) hts_close(self->pfile);
    if (self->record) bcf_destroy(self->record);
    if (self->type_strings) {
        for (unsigned int i=0; i<NUM_TYPES; i++) Py_XDECREF(self->type_strings[i]);
        free(self->type_strings);
    }
    if (self->error_strings) {
        for (unsigned int i=0; i<NUM_ERRORS; i++) Py_XDECREF(self->error_strings[i]);
        free(self->error_strings);
    }
    if (self->p_int) free(self->p_int);
    if (self->gt_p) free(self->gt_p);
    if (self->p_float) free(self->p_float);
    if (self->p_str) free(self->p_str);
    Py_TYPE(self)->tp_free((PyObject *) self);
}

// NEW METHOD
static PyObject * VCF_new(PyTypeObject * type, PyObject * args, PyObject * kwds) {
    VCF_object * self;
    self = (VCF_object *) type->tp_alloc(type, 0);
    if (!self) return NULL;
    self->record = bcf_init();
    if (!self->record) return NULL;
    self->type_strings = (PyObject **) malloc(NUM_TYPES * sizeof(PyObject *));
    if (!self->type_strings) {
        PyErr_NoMemory();
        return NULL;
    }
    for (unsigned int i=0; i<NUM_TYPES; i++) {
        self->type_strings[i] = NULL;
    }
    for (unsigned int i=0; i<NUM_TYPES; i++) {
        self->type_strings[i] = PyUnicode_FromString(TYPENAMES[i]);
        if (self->type_strings[i] == NULL) return NULL;
    }
    self->error_strings = (PyObject **) malloc(NUM_ERRORS * sizeof(PyObject *));
    if (!self->error_strings) {
        PyErr_NoMemory();
        return NULL;
    }
    for (unsigned int i=0; i<NUM_ERRORS; i++) {
        self->error_strings[i] = NULL;
    }
    for (unsigned int i=0; i<NUM_ERRORS; i++) {
        self->error_strings[i] = PyUnicode_FromString(ERRORNAMES[i]);
        if (self->error_strings[i] == NULL) return NULL;
    }
    self->pfile = NULL;
    self->hdr = NULL;
    self->num_samples = 0;
    self->status = 0;
    self->p_int = NULL;
    self->n_int = 0;
    self->p_float = NULL;
    self->n_float = 0;
    self->p_str = NULL;
    self->n_str = 0;
    self->gt_p = NULL;
    self->gt_n = 0;
    self->gt_num = 0;
    self->index = NULL;
    self->has_index = 0;
    return (PyObject *) self;
}

// INIT METHOD: open file, read header
static int VCF_init(VCF_object * self, PyObject * args, PyObject * kwds) {
    int res = 0;
    char * fname;
    char * index = NULL;

    static char *kwlist[] = {"fname", "index", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "s|s", kwlist, &fname, &index)) {
        return -1;
    }

    self->pfile = hts_open(fname, "r");
    if (!self->pfile) {
        res = -1;
    }
    else {
        self->hdr = bcf_hdr_read(self->pfile);
        if (!self->hdr) res = -1;
        else {
            self->num_samples = bcf_hdr_nsamples(self->hdr);
        }
    }
    
    if (res != 0) {
        PyErr_SetString(PyExc_ValueError, "Cannot open file");
        return res;
    }

    if (index) {
        self->index = bcf_index_load2(fname, index);
        if (!self->index) {
            PyErr_SetString(PyExc_ValueError, "Cannot import index");
            return -1;
        }
        self->has_index = 1;
    }
    else {
        self->index = bcf_index_load(fname);
        self->has_index = self->index != NULL;
    }

    return res;
}

/************************************
    READ A LINE
 ************************************/

void read_success(VCF_object * self) {
    self->types = bcf_get_variant_types(self->record);
    self->status = 1;
    self->gt_num = 0;
} // this method set so variant upon reading a variant (for read() and goto())

static PyObject * VCF_read(VCF_object * self, PyObject * Py_UNUSED(ignored)) {
    self->status = 0; // in case an error/EOF occurs
    int res = bcf_read(self->pfile, self->hdr, self->record);
    if (res == -1) Py_RETURN_FALSE;
    if (res != 0) {
        PyErr_SetString(PyExc_OSError, "Critical error while reading a variant");
        return NULL;
    }

    read_success(self);
    Py_RETURN_TRUE;
}

/************************************
    NAVIGATION
    (indexed bcf files)
 ************************************/

static PyObject * VCF_goto(VCF_object * self, PyObject * args) {
    if (!self->has_index) {
        PyErr_SetString(PyExc_ValueError, "An index is required");
        return NULL;
    }

    const char * target;
    int pos = 0;
    if (!PyArg_ParseTuple(args, "s|i", &target, &pos)) {
        return NULL;
    }

    int tid = bcf_hdr_name2id(self->hdr, target);
    if (tid < 0) {
        PyErr_SetString(PyExc_ValueError, "Unknown target name");
        return NULL;
    }

    hts_itr_t * itr = bcf_itr_queryi(self->index, tid, pos, INT_MAX);
    if (itr == NULL) {
        PyErr_SetString(PyExc_ValueError, "Cannot create iterator");
        return NULL;
    }

    int res = bcf_itr_next(self->pfile, itr, self->record);
    hts_itr_destroy(itr);

    if (res == -1) Py_RETURN_FALSE;
    if (res < 0) {
        PyErr_SetString(PyExc_ValueError, "A reading error occurred");
        return NULL;
    }

    read_success(self);
    Py_RETURN_TRUE;
}

/*******************************************
    ACCESS METHODS
    (require that header was read
     -- always the case if object created)
 *******************************************/

static PyObject * VCF_get_sample(VCF_object * self, PyObject * args) {
    int idx = 0;
    if (!PyArg_ParseTuple(args, "i", &idx)) {
        return NULL;
    }
    if (idx < 0) idx += self->num_samples;
    if (idx < 0 || idx >= self->num_samples) {
        PyErr_SetString(PyExc_IndexError, "sample index out of range");
        return NULL;
    }
    return PyUnicode_FromString(self->hdr->samples[idx]);
}

/************************************
    ACCESS METHODS
    (require that a line was read)
 ************************************/

// extract polymorphic type names from the flag
static PyObject * VCF_get_types(VCF_object * self, PyObject * Py_UNUSED(ignored)) {
    if (self->status == 0) Py_RETURN_NONE;
    PyObject * set = PySet_New(NULL);
    for (unsigned int i=0; i<NUM_TYPES; i++) {
        if (self->types & TYPES[i]) {
            Py_INCREF(self->type_strings[i]);
            if (PySet_Add(set, self->type_strings[i]) != 0) return NULL;
        }
    }
    return set;
}

// extract error names from the flag
static PyObject * VCF_get_errors(VCF_object * self, PyObject * Py_UNUSED(ignored)) {
    if (self->status == 0) Py_RETURN_NONE;
    PyObject * set = PySet_New(NULL);
    for (unsigned int i=0; i<NUM_ERRORS; i++) {
        if (self->record->errcode & ERRORS[i]) {
            Py_INCREF(self->error_strings[i]);
            if (PySet_Add(set, self->error_strings[i]) != 0) return NULL;
        }
    }
    return set;
}

// return a boolean to say if the polymorphism is SNP (and SNP only)
static PyObject * VCF_is_snp(VCF_object * self, PyObject * Py_UNUSED(ignored)) {
    if (self->status == 0) Py_RETURN_FALSE;
    return PyBool_FromLong(self->types == VCF_SNP);
}

// get chromosome name
static PyObject * VCF_get_chrom(VCF_object * self, PyObject * Py_UNUSED(ignored)) {
    if (self->status == 0) Py_RETURN_NONE;
    return PyUnicode_FromString(bcf_hdr_id2name(self->hdr, self->record->rid));
}

// get position
static PyObject * VCF_get_pos(VCF_object * self, PyObject * Py_UNUSED(ignored)) {
    if (self->status == 0) Py_RETURN_NONE;
    return PyLong_FromLong(self->record->pos);
}

// get quality
static PyObject * VCF_get_qual(VCF_object * self, PyObject * Py_UNUSED(ignored)) {
    bcf_unpack(self->record, BCF_UN_FLT); // necessary?
    if (self->status == 0 || bcf_float_is_missing(self->record->qual)) Py_RETURN_NONE;
    return PyFloat_FromDouble(self->record->qual);
}

// get reference allele
static PyObject * VCF_get_ref(VCF_object * self, PyObject * Py_UNUSED(ignored)) {
    if (self->status == 0) Py_RETURN_NONE;
    bcf_unpack(self->record, BCF_UN_STR);
    if (self->record->n_allele == 0) Py_RETURN_NONE;
    return PyUnicode_FromString(self->record->d.allele[0]);
}

// get list of alternate allele(s)
static PyObject * VCF_get_alt(VCF_object * self, PyObject * Py_UNUSED(ignored)) {
    if (self->status == 0) Py_RETURN_NONE;
    bcf_unpack(self->record, BCF_UN_STR);
    if (self->record->n_allele < 2) Py_RETURN_NONE;
    PyObject * list = PyList_New(self->record->n_allele-1);
    if (list) {
        for (unsigned int i=1; i<self->record->n_allele; i++) {
            PyObject * item = PyUnicode_FromString(self->record->d.allele[i]);
            if (item) PyList_SET_ITEM(list, i-1, item);
            else return NULL; // also: decref list?
        }
    }
    return list;
}

// get set of filter values
static PyObject * VCF_get_filter(VCF_object * self, PyObject * Py_UNUSED(ignored)) {
    if (self->status == 0) Py_RETURN_NONE;
    bcf_unpack(self->record, BCF_UN_FLT);
    PyObject * set = PySet_New(NULL);
    for (int i=0; i<self->record->d.n_flt; i++) {
        if (PySet_Add(set, PyUnicode_FromString(bcf_hdr_int2id(self->hdr, BCF_DT_ID, self->record->d.flt[i]))) != 0) return NULL;
    }
    return set;
}

// get a given info value (as a string, int, float or list of int or float)
static PyObject * VCF_get_info(VCF_object * self, PyObject * args) {
    if (self->status == 0) Py_RETURN_NONE;
    bcf_unpack(self->record, BCF_UN_INFO);

    char * tag;
    int num, info_id;
    PyObject * item, *list;

    // get tag from argument
    if (!PyArg_ParseTuple(args, "s", &tag)) {
        return NULL;
    }

    // get info specification (the info must be defined in the header)
    info_id = bcf_hdr_id2int(self->hdr, BCF_DT_ID, tag);
    if (info_id < 0) {
        PyErr_SetString(PyExc_ValueError, "Invalid info key");
        return NULL;
    }

    // avoid duplication of operations
    #define int_is_missing(x) (x==bcf_int32_missing)
    #define PROCESS(getter, p, n, Py, missing) { \
        num = getter(self->hdr, self->record, tag, &p, &n); \
        if (num == -3) Py_RETURN_NONE; \
        if (num < 0) { \
            PyErr_SetString(PyExc_ValueError, "Cannot import INFO data"); \
            return NULL; \
        } \
        if (num == 1 && bcf_hdr_id2number(self->hdr, BCF_HL_INFO, info_id) == 1) { \
            if (missing(p[0])) Py_RETURN_NONE; \
            else return Py(p[0]); \
        } \
        else { \
            list = PyList_New(num); \
            if (!list) return NULL; \
            for (int idx=0; idx<num; idx++) { \
                if (missing(p[idx])) { \
                    Py_INCREF(Py_None); \
                    item = Py_None; \
                } \
                else { \
                    item = Py(p[idx]); \
                    if (!item) return NULL; \
                } \
                PyList_SET_ITEM(list, idx, item); \
            } \
            return list; \
        } \
    }

    // process field by type
    switch (bcf_hdr_id2type(self->hdr, BCF_HL_INFO, info_id)) {
        case BCF_HT_FLAG:
            num = bcf_get_info_flag(self->hdr, self->record, tag, NULL, NULL);
            if (num == -3) Py_RETURN_NONE;
            if (num < 0) {
                PyErr_SetString(PyExc_ValueError, "Cannot import INFO data");
                return NULL;
            }
            item = PyBool_FromLong(num);
            if (!item) return NULL;
            return item;
        case BCF_HT_INT:
            PROCESS(bcf_get_info_int32, self->p_int, self->n_int, PyLong_FromLong, int_is_missing);
        case BCF_HT_REAL:
            PROCESS(bcf_get_info_float, self->p_float, self->n_float, PyFloat_FromDouble, bcf_float_is_missing);
        case BCF_HT_STR:
            num = bcf_get_info_string(self->hdr, self->record, tag, &self->p_str, &self->n_str);
            if (num == -3) Py_RETURN_NONE;
            if (num < 0) {
                PyErr_SetString(PyExc_ValueError, "Cannot import INFO data");
                return NULL;
            }
            item = PyUnicode_FromString(self->p_str);
            if (!item) return NULL;
            return item;
        default:
            PyErr_SetString(PyExc_RuntimeError, "Cannot process info type");
            return NULL;
    }
    #undef int_is_missing
    #undef PROCESS
    Py_RETURN_NONE; // should be unused
}

// get a given format value
static PyObject * VCF_get_format(VCF_object * self, PyObject * args) {
    if (self->status == 0) Py_RETURN_NONE;
    bcf_unpack(self->record, BCF_UN_FMT);

    const char * tag, * p;
    int idx, i, format_id, res, num, L;
    PyObject * list, *item;

    // get arguments
    if (!PyArg_ParseTuple(args, "si", &tag, &idx)) {
        return NULL;
    }

    if (idx < 0) idx += self->num_samples;
    if (idx < 0 || idx >= self->num_samples) {
        PyErr_SetString(PyExc_IndexError, "sample index out of range");
        return NULL;
    }

    // get format specification (the format must be defined in the header)
    format_id = bcf_hdr_id2int(self->hdr, BCF_DT_ID, tag);
    if (format_id < 0) {
        PyErr_SetString(PyExc_ValueError, "Invalid format key");
        return NULL;
    }

    // avoid duplication of operations
    #define int_is_missing(x) (x==bcf_int32_missing)
    #define int_is_vector_end(x) (x==bcf_int32_vector_end)
    #define PROCESS(getter, p, n, Py, missing, vector_end) { \
        res = getter(self->hdr, self->record, tag, &p, &n); \
        if (res == -3) Py_RETURN_NONE; \
        if (res < 1) { \
            PyErr_SetString(PyExc_ValueError, "Cannot import FORMAT data"); \
            return NULL; \
        } \
        if (res < self->num_samples) { \
            PyErr_SetString(PyExc_ValueError, "Cannot import FORMAT data (invalid number of items)"); \
            return NULL; \
        } \
        num = res/self->num_samples; \
        if (num == 1 && bcf_hdr_id2number(self->hdr, BCF_HL_FMT, format_id) == 1) { \
            if (missing(p[idx])) Py_RETURN_NONE; \
            else return Py(p[idx]); \
        } \
        else { \
            list = PyList_New(0); \
            if (!list) return NULL; \
            for (i=0; i<num; i++) { \
                if (vector_end(p[idx*num+i])) break;\
                if (missing(p[idx*num+i])) { \
                    Py_INCREF(Py_None); \
                    item = Py_None; \
                } \
                else { \
                    item = Py(p[idx*num+i]); \
                    if (!item) { \
                        Py_DECREF(list); \
                        return NULL; \
                    } \
                } \
                if (PyList_Append(list, item) != 0) { \
                    Py_DECREF(list); \
                    return NULL; \
                } \
            } \
            return list; \
        } \
    }

    // process field by type
    switch (bcf_hdr_id2type(self->hdr, BCF_HL_FMT, format_id)) {
        case BCF_HT_INT:
            PROCESS(bcf_get_format_int32, self->p_int, self->n_int, PyLong_FromLong, int_is_missing, int_is_vector_end);
        case BCF_HT_REAL:
            PROCESS(bcf_get_format_float, self->p_float, self->n_float, PyFloat_FromDouble, bcf_float_is_missing, bcf_float_is_vector_end);
        case BCF_HT_STR:
            res = bcf_get_format_char(self->hdr, self->record, tag, &self->p_str, &self->n_str);
            if (res == -3) Py_RETURN_NONE;
            if (res < self->num_samples) {
                PyErr_SetString(PyExc_ValueError, "Cannot import FORMAT data");
                return NULL;
            }
            num = res / self->num_samples;
            p = strchr(self->p_str+idx*num, '\0');
            if (p == NULL) L = num;
            else L = strchr(self->p_str+idx*num, '\0')-(self->p_str+idx*num);
            item = PyUnicode_FromStringAndSize(self->p_str+idx*num, L);
            if (!item) return NULL;
            return item;
        default:
            PyErr_SetString(PyExc_RuntimeError, "Cannot process format type");
            return NULL;
    }
    #undef int_is_missing
    #undef int_is_vector_end
    #undef PROCESS
    Py_RETURN_NONE; // should be unused
}

// get all info values
static PyObject * VCF_get_infos(VCF_object * self, PyObject * Py_UNUSED(ignored)) {
    if (self->status == 0) Py_RETURN_NONE;
    bcf_unpack(self->record, BCF_UN_INFO);

    PyObject * dict = PyDict_New();
    if (dict == NULL) return NULL;

    PyObject * key, *value, *args;
    const char * tag;

    for (unsigned int idx=0; idx<self->record->n_info; idx++) {

        // get key
        tag = self->hdr->id[BCF_DT_ID][self->record->d.info[idx].key].key;

        key = PyUnicode_FromString(tag);
        if (!key) return NULL;

        // get value
        args = Py_BuildValue("(s)", tag);
        if (!args) return NULL;
        value = VCF_get_info(self, args);
        Py_DECREF(args);
        if (value == NULL) return NULL;
        if (PyDict_SetItem(dict, key, value) != 0) {
            Py_DECREF(dict);
            Py_DECREF(key);
            Py_DECREF(value);
            return NULL;
        }
        Py_DECREF(key);
        Py_DECREF(value);
    }

    return dict;
}

// get all format values for all samples
static PyObject * VCF_get_formats(VCF_object * self, PyObject * Py_UNUSED(ignored)) {
    if (self->status == 0) Py_RETURN_NONE;
    bcf_unpack(self->record, BCF_UN_FMT);

    PyObject * list = PyList_New(self->num_samples);
    if (!list) return NULL;

    PyObject * dict;
    PyObject * key, *value, *args;
    const char * tag;

    for (int sam=0; sam<self->num_samples; sam++) {

        dict = PyDict_New();
        if (dict == NULL) {
            Py_DECREF(list);
            return NULL;
        }
        for (unsigned int fmt=0; fmt<self->record->n_fmt; fmt++) {

            // get key
            tag = self->hdr->id[BCF_DT_ID][self->record->d.fmt[fmt].id].key;
            if (!strcmp(tag, "GT")) continue;

            key = PyUnicode_FromString(tag);
            if (!key) {
                Py_DECREF(list);
                Py_DECREF(dict);
                return NULL;
            }

            // get value
            args = Py_BuildValue("(si)", tag, sam);
            if (!args) return NULL;
            value = VCF_get_format(self, args);
            Py_DECREF(args);
            if (value == NULL) {
                Py_DECREF(list);
                Py_DECREF(dict);
                Py_DECREF(key);
                return NULL;
            }
            if (PyDict_SetItem(dict, key, value) != 0) {
                Py_DECREF(list);
                Py_DECREF(dict);
                Py_DECREF(key);
                Py_DECREF(value);
                return NULL;
            }
            Py_DECREF(key);
            Py_DECREF(value);
        }
        if (PyList_SET_ITEM(list, sam, dict));
    }

    return list;
}

// get all GT values for the last site
static int VCF_get_GT(VCF_object * self) {
    if (self->status == 0) return 0;
    bcf_unpack(self->record, BCF_UN_FMT);
    int ngt = bcf_get_genotypes(self->hdr, self->record, &self->gt_p, &self->gt_n);
    if (ngt <= 0) return 0;
    self->gt_num = ngt/self->num_samples;
    return 1;
}

static PyObject * VCF_get_genotypes(VCF_object * self, PyObject * Py_UNUSED(ignored)) {
    if (self->gt_num == 0 && VCF_get_GT(self) == 0) Py_RETURN_NONE;

    int i, j;
    int32_t * p;
    PyObject * list, * item, * value;
    list = PyList_New(self->num_samples);
    if (!list) return NULL;

    for (i=0; i<self->num_samples; i++) {
        item = PyList_New(0);
        if (!item) {
            Py_DECREF(list);
            return NULL;
        }
        p = self->gt_p + i * self->gt_num;
        for (j=0; j<self->gt_num; j++) {
            if (p[j] == bcf_int32_vector_end) break; // sample has smaller ploidy
            if (bcf_gt_is_missing(p[j])) { // missing allele
                Py_INCREF(Py_None);
                if (PyList_Append(item, Py_None) != 0) {
                    Py_DECREF(list);
                    Py_DECREF(item);
                    return NULL;
                }
                continue;
            }
            value = PyUnicode_FromString(self->record->d.allele[bcf_gt_allele(p[j])]);
            if (!value) {
                Py_DECREF(list);
                Py_DECREF(item);
                return NULL;
            }

            if (PyList_Append(item, value) != 0) {
                Py_DECREF(list);
                Py_DECREF(item);
                Py_DECREF(value);
                return NULL;
            }
        }
        PyList_SET_ITEM(list, i, item);
    }
    return list;
}

static PyObject * VCF_get_phased(VCF_object * self, PyObject * Py_UNUSED(ignored)) {
    if (self->gt_num == 0 && VCF_get_GT(self) == 0) Py_RETURN_NONE;

    int i, j, all_b = 1;
    int32_t * p;
    PyObject * ret_tuple, * list, * item, * boolean, * all_phased;
    list = PyList_New(self->num_samples);
    if (!list) return NULL;

    for (i=0; i<self->num_samples; i++) {
        item = PyList_New(0);
        if (!item) {
            Py_DECREF(list);
            return NULL;
        }
        p = self->gt_p + i * self->gt_num;
        for (j=1; j<self->gt_num; j++) {
            if (p[j] == bcf_int32_vector_end) break; // sample has smaller ploidy
            if (bcf_gt_is_missing(p[j])) { // missing allele
                Py_INCREF(Py_None);
                if (PyList_Append(item, Py_None) != 0) {
                    Py_DECREF(list);
                    Py_DECREF(item);
                    return NULL;
                }
                continue;
            }
            all_b &= bcf_gt_is_phased(p[j]);
            boolean = PyBool_FromLong(bcf_gt_is_phased(p[j]));
            if (!boolean) {
                Py_DECREF(list);
                Py_DECREF(item);
                return NULL;
            }

            if (PyList_Append(item, boolean) != 0) {
                Py_DECREF(list);
                Py_DECREF(item);
                Py_DECREF(boolean);
                return NULL;
            }
        }
        PyList_SET_ITEM(list, i, item);
    }

    all_phased = PyBool_FromLong(all_b);
    if (!all_phased) {
        Py_DECREF(list);
        return NULL;
    }

    ret_tuple = PyTuple_New(2);
    if (!ret_tuple){
        Py_DECREF(list);
        Py_DECREF(all_phased);
        return NULL;
    }
    PyTuple_SET_ITEM(ret_tuple, 0, all_phased);
    PyTuple_SET_ITEM(ret_tuple, 1, list);

    return ret_tuple;
}

/************************************
    DEFINITION OF PYTHON TYPE
 ************************************/

// methods
static PyMethodDef VCF_methods[] = {
    {"read",          (PyCFunction) VCF_read,          METH_NOARGS,  "Read one variant of the VCF file (``True`` if read is successful, ``False`` if end of file)."},
    {"get_sample",    (PyCFunction) VCF_get_sample,    METH_VARARGS, "get_sample(index)\nGet the name of a sample."},
    {"get_errors",    (PyCFunction) VCF_get_errors,    METH_NOARGS,  "Get the non-fatal errors generated while importing last variant, as a set, or ``None`` if nothing has been read."},
    {"get_types",     (PyCFunction) VCF_get_types,     METH_NOARGS,  "Get the type(s) of the last variant, as a set, or ``None`` if nothing has been read."},
    {"is_snp",        (PyCFunction) VCF_is_snp,        METH_NOARGS,  "``True`` if the last variant is of type SNP (and no other)."},
    {"get_quality",   (PyCFunction) VCF_get_qual,      METH_NOARGS,  "Quality value, or ``None`` if nothing has been read or if the value is missing."},
    {"get_chrom",     (PyCFunction) VCF_get_chrom,     METH_NOARGS,  "Chromosome name, or ``None`` if nothing has been read."},
    {"get_pos",       (PyCFunction) VCF_get_pos,       METH_NOARGS,  "Position, or ``None`` if nothing has been read."},
    {"get_reference", (PyCFunction) VCF_get_ref,       METH_NOARGS,  "Reference allele, as a string, or ``None`` if nothing has been read."},
    {"get_alternate", (PyCFunction) VCF_get_alt,       METH_NOARGS,  "List of alternate alleles, or ``None`` if nothing has been read."},
    {"get_filter",    (PyCFunction) VCF_get_filter,    METH_NOARGS,  "Get the filters defined for the last variant as a set, or ``None`` if nothing has been read."},
    {"get_infos",     (PyCFunction) VCF_get_infos,     METH_NOARGS,  "Get the info field for the last variant as a dict, or ``None`` if nothing has been read."},
    {"get_formats",   (PyCFunction) VCF_get_formats,   METH_NOARGS,  "Get the format field (except GT) all samples as a list of dict, or ``None`` if nothing has been read."},
    {"get_info",      (PyCFunction) VCF_get_info,      METH_VARARGS, "get_info(tag)\nGet a given info field (``None`` if nothing has been read or if the key is not available)."},
    {"get_format",    (PyCFunction) VCF_get_format,    METH_VARARGS, "get_format(tag, index)\nGet a given format field (``None`` if nothing has been read or if the key is not available)."},
    {"get_genotypes", (PyCFunction) VCF_get_genotypes, METH_NOARGS,  "Get genotypes (``None`` whatever bad happens)."},
    {"get_phased",    (PyCFunction) VCF_get_phased,    METH_NOARGS,  "Get a tuple (all_phased, phased_table) (``None`` whatever bad happens)."},
    {"goto",          (PyCFunction) VCF_goto,          METH_VARARGS, "goto(target[, position])\nMove to a given location and read the position (?) ValueError whatever wrong happens."},
    {NULL, NULL, 0, NULL}
};

// simple members
static PyMemberDef VCF_members[] = {
    {"num_samples", T_INT, offsetof(VCF_object, num_samples), READONLY, "Number of samples."},
    {"has_index", T_BOOL, offsetof(VCF_object, has_index), READONLY, "Boolean indicating whether an index is available."},
    {NULL}
};

// type
static PyTypeObject VCF = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "_vcf.VCF",
    .tp_doc = "VCF/BCF file pointer",
    .tp_basicsize = sizeof(VCF_object),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = VCF_new,
    .tp_init = (initproc) VCF_init,
    .tp_dealloc = (destructor) VCF_dealloc,
    .tp_methods = VCF_methods,
    .tp_members = VCF_members,
};

/************************************
    MODULE CONFIGURATION
 ************************************/

static PyMethodDef vcf_methods[] = {
    {"index_vcf", (PyCFunction)(void(*)(void))vcf_index_vcf, METH_VARARGS | METH_KEYWORDS, "index_vcf(fname[, outname])\nIndex a BCF file."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef vcfmodule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "_vcf",
    .m_doc = "VCF/BCF parser using HTSlib",
    .m_size = -1,
    vcf_methods
};

// module initialisation function
PyMODINIT_FUNC PyInit__vcf(void) { // N.B. double underscore because the module name is _vcf
    PyObject * m;
    if (PyType_Ready(&VCF) < 0) return NULL;

    m = PyModule_Create(&vcfmodule);
    if (!m) return NULL;

    // add the VCF type to the module
    Py_INCREF(&VCF);
    if (PyModule_AddObject(m, "VCF", (PyObject *) &VCF) < 0) {
        Py_DECREF(&VCF);
        Py_DECREF(m);
        return NULL;
    }

    hts_set_log_level(HTS_LOG_OFF); // prevent htslib log messages in case of errors/warnings
    return m;
}
