#include <Python.h>
#include "structmember.h"

#include "mydouble.h"

//TODO: __add__ and __radd__

static long count = 0, freed = 0;

static void
mydouble_dealloc(mydouble* self) {
  self->ob_type->tp_free((PyObject*)self);
  freed += 1;
  count -= 1;
}

static inline PyObject *
mydouble_alloc() //PyTypeObject *type) 
{
  count += 1;
  return PyType_GenericAlloc(&mydoubleType, 0);
}

static PyObject *as_double(PyObject *arg, double *v) {
  if (Py_TYPE(arg) != &mydoubleType) {
    if (Py_TYPE(arg)->tp_as_number && Py_TYPE(arg)->tp_as_number->nb_float)
        *v = PyFloat_AsDouble(arg);
    else
      return NULL;
  }
  else
    *v = ((mydouble *)arg)->value;

  return arg;
}

static PyObject *
mydouble_new(PyTypeObject *type, PyObject *args)
{
    mydouble *self = mydouble_alloc();//type);

/*     // "|..." means optional (otherwise error); default value is 0 */
/*     if (!PyArg_ParseTuple(args, "|d", &(self->value))) */
/*       return NULL;     */
   // the following is from Cython, faster than parsetuple
   switch (PyTuple_GET_SIZE(args)) {
   case  0: break;
   case  1: 
     if (!as_double(PyTuple_GET_ITEM(args, 0), &self->value))
       return NULL;
     break; // !!
   case 2: // pair (value, second)
     if (!as_double(PyTuple_GET_ITEM(args, 0), &self->value) 
         || !as_double(PyTuple_GET_ITEM(args, 1), &self->second))
       return NULL;
     break; // !!
   default: return NULL;
   }
    return (PyObject *)self;
}

// actually deepcopy (doesn't make sense to do shallow copy: pointer copy?)
static PyObject *
mydouble_copy(mydouble *self) {
  // must pass a tuple (d), not a number! (args is parsed by py_parsetupe)
  mydouble *s = mydouble_alloc();//Py_TYPE(self)); 
  s->value = self->value;
  return s;  
}

static PyObject *
mydouble_deepcopy(mydouble *self, PyObject *args) {
  // args is for memo; neglected
  return mydouble_copy(self);
}

// __iadd__: works with either mydouble or anything convertable to mydouble
static PyObject *
mydouble_iadd(mydouble *self, PyObject *arg) {
  
  static double value = 0;
  if (!as_double(arg, &value))
    return NULL;
  self->value += value;
  Py_INCREF(self); // important for __iadd__
  return self;
}

// __add__: returns mydouble type
static PyObject *
mydouble_add(mydouble *self, PyObject *arg) {
  
  static double value = 0;
  if (!as_double(arg, &value))
    return NULL;
  mydouble *s = mydouble_alloc();//Py_TYPE(self)); 
  s->value = self->value + value;
  return s;
}

/* // __radd__: returns Python float # no effect here */
/* static PyObject * */
/* mydouble_radd(mydouble *self, PyObject *arg) { */
/*   return PyNumber_Add(self, arg); */
/* } */

static PyObject *
mydouble_incr(mydouble *self) {

  self->value += 1;
  Py_RETURN_NONE;
}

static PyObject *
mydouble_decr(mydouble *self) {

  self->value -= 1;
  Py_RETURN_NONE;
}

static PyObject *
mydouble_float(mydouble *self) {
  //  return Py_BuildValue("d", self->value);
  return PyFloat_FromDouble(self->value);
}

static PyObject *
mydouble_pair(mydouble *self) {
  return Py_BuildValue("(dd)", self->value, self->second);
}

static PyObject *format;

static PyObject *
mydouble_str(mydouble *self) {        

  // TODO: further speedup: cache str results

  // from Python/Objects/floatobject.c:float_str_or_repr()
  // N.B.: 'r' is a char, not a char * ("...") in C!
  //       'r' means 'repr' style. ADD_DOT to distinguish with int.

  PyObject *result;
  char *buf = PyOS_double_to_string(self->value,
				    'r', 0,
				    Py_DTSF_ADD_DOT_0,
				    NULL);

  result = PyString_FromString(buf);
  PyMem_Free(buf);
  return result;
}

static int
mydouble_cmp(mydouble *self, mydouble *other) {
  // TODO: do we need fabs < 1e-6?
  double d = self->value - other->value;
  return (d==0)? 0 : (d>0?1:-1); 
}

// important for pickling
static PyObject *
mydouble_reduce(mydouble *self) {
  PyObject * result, *args;
  args = Py_BuildValue("(d)", self->value);
  result = PyTuple_Pack(2, Py_TYPE(self), args); // None's are optional
  Py_DECREF(args); // important for mem!
  return result;
}

static PyMethodDef mydouble_methods[] = {
    {"float", (PyCFunction)mydouble_float, METH_NOARGS, "to python float"},
    {"str", (PyCFunction)mydouble_str, METH_NOARGS, "to string"},
    {"incr", (PyCFunction)mydouble_incr, METH_NOARGS, "(void) +=1"},
    {"decr", (PyCFunction)mydouble_decr, METH_NOARGS, "(void) -=1"},
    {"copy", (PyCFunction)mydouble_copy, METH_NOARGS, "deepcopy!"},
    {"__copy__", (PyCFunction)mydouble_copy, METH_NOARGS, "deepcopy!"},
    {"__deepcopy__", (PyCFunction)mydouble_deepcopy, METH_O, "deepcopy"},
    {"__reduce__", (PyCFunction)mydouble_reduce, METH_NOARGS, "for pickle"},
    {"pair", (PyCFunction)mydouble_pair, METH_NOARGS, "to python tuple (pair of doubles)"},
    //    {"__add__", (PyCFunction)mydouble_add, METH_O, "returns mydouble"},
    //    {"__radd__", (PyCFunction)mydouble_radd, METH_O, "returns float"},
    {NULL}  /* Sentinel */
};

static PyNumberMethods mydouble_as_number = {
    mydouble_add,          /*nb_add*/
    0,          /*nb_subtract*/
    0,          /*nb_multiply*/
    0, /*nb_divide*/
    0,          /*nb_remainder*/
    0,       /*nb_divmod*/
    0,          /*nb_power*/
    0, /*nb_negative*/
    0, /*nb_positive*/
    0, /*nb_absolute*/
    0, /*nb_nonzero*/
    0,                  /*nb_invert*/
    0,                  /*nb_lshift*/
    0,                  /*nb_rshift*/
    0,                  /*nb_and*/
    0,                  /*nb_xor*/
    0,                  /*nb_or*/
    0,       /*nb_coerce*/
    0,        /*nb_int*/
    0,         /*nb_long*/
    mydouble_float,        /*nb_float*/
    0,                  /* nb_oct */
    0,                  /* nb_hex */
    mydouble_iadd,     /* nb_inplace_add */
    0,                  /* nb_inplace_subtract */
    0,                  /* nb_inplace_multiply */
    0,                  /* nb_inplace_divide */
    0,                  /* nb_inplace_remainder */
    0,                  /* nb_inplace_power */
    0,                  /* nb_inplace_lshift */
    0,                  /* nb_inplace_rshift */
    0,                  /* nb_inplace_and */
    0,                  /* nb_inplace_xor */
    0,                  /* nb_inplace_or */
    0, /* nb_floor_divide */
    0,          /* nb_true_divide */
    0,                  /* nb_inplace_floor_divide */
    0                  /* nb_inplace_true_divide */
};

static PyTypeObject mydoubleType = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "mydouble",             /*tp_name*/
    sizeof(mydouble),             /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor)mydouble_dealloc, /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    (cmpfunc)mydouble_cmp,     /*tp_compare*/
    (reprfunc)mydouble_str,    /*tp_repr*/
    &mydouble_as_number,        /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    0,                         /*tp_call*/
    (reprfunc)mydouble_str,    /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_CHECKTYPES, /*tp_flags -- checktypes for __[r]add__*/
    "mydouble objects",           /* tp_doc */
    0,		               /* tp_traverse */
    0,		               /* tp_clear */
    0,		               /* tp_richcompare */
    0,		               /* tp_weaklistoffset */
    0,		               /* tp_iter */
    0,		               /* tp_iternext */
    mydouble_methods,             /* tp_methods */
    0,             /* tp_members */
    0,                         /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    0,      /* tp_init */
    mydouble_alloc,                         /* tp_alloc */
    mydouble_new,                 /* tp_new */
};

static PyObject *counts(PyObject *self)
{
  return Py_BuildValue("(ii)", count, freed);
}

static PyMethodDef module_methods[] = {
  {"counts", counts, METH_NOARGS, "return counts (mem usage)"}, 
  {NULL}  /* Sentinel */
};

#ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC
initmydouble(void) 
{
    PyObject* m;

    format = PyString_FromString("%s");
    if (PyType_Ready(&mydoubleType) < 0)
        return;

    m = Py_InitModule3("mydouble", module_methods,
                       "Example module that creates an extension type.");

    if (m == NULL)
      return;

    Py_INCREF(&mydoubleType);
    PyModule_AddObject(m, "mydouble", (PyObject *)&mydoubleType);
}
