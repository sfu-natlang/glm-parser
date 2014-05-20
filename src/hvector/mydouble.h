#include <Python.h>
#include "structmember.h"

//#define double float

typedef struct {
    PyObject_HEAD
    double value;
  double second; // avg/all weights
} mydouble;

static PyObject *
mydouble_copy(mydouble *self);

static PyTypeObject mydoubleType;

static PyObject *
mydouble_new(PyTypeObject *type, PyObject *args);
