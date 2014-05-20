#include "Python.h"
#include "structmember.h"
#include "dictobject.h"

#include "mydouble.h"

// DONE: separate deepcopy and copy, pyobject_setitem and pydict_setitem
// TODO: merge with mydouble.c, so that i no longer need new_mydouble here
// TODO: integrate fast pickling
PyTypeObject *mydouble_type = NULL;

/////////////////
/* collections module implementation of a deque() datatype
   Written and maintained by Raymond D. Hettinger <python@rcn.com>
   Copyright (c) 2004 Python Software Foundation.
   All rights reserved.
*/

/* The block length may be set to any number over 1.  Larger numbers
 * reduce the number of calls to the memory allocator but take more
 * memory.  Ideally, BLOCKLEN should be set with an eye to the
 * length of a cache line.
 */

#define BLOCKLEN 62
#define CENTER ((BLOCKLEN - 1) / 2)

/* defaultdict type *********************************************************/

typedef struct {
  PyDictObject dict;
  PyObject *default_factory;
  double step_c;  
} defdictobject;

static PyTypeObject defdict_type; /* Forward */

static mydouble *
new_mydouble(double v) //defdictobject *dd, PyObject *key)
{
  //  return PyEval_CallObject(dd->default_factory, NULL);
  // TODO: after merging with mydouble.c, call alloc directly
  mydouble *s = mydouble_type->tp_alloc(mydouble_type, 0);
  s->value = v;
  return s;
}

static PyObject *
defdict_missing_add(defdictobject *dd, PyObject *key)
{
  PyObject *value = new_mydouble(0); //defdict_missing(); // no insert
  // lhuang
  // CAUTION: only use PyDict_SetItem, not PyObject_SetItem 
  // (which calls this my own mydefdict_setitem defined below)!

  if (PyDict_SetItem((PyObject *)dd, key, value) < 0) {
    Py_DECREF(value);
    return NULL;
  }
  return value;
}

// shallow copy
static PyObject *
defdict_copy(defdictobject *self)
{
    /* This calls the object's class.  That only works for subclasses
       whose class constructor has the same signature.  Subclasses that
       define a different constructor signature must override copy().
    */

  // copy of defdict
    PyObject *new = PyObject_CallFunctionObjArgs((PyObject*)Py_TYPE(self),
						 self->default_factory, NULL, NULL);

    Py_ssize_t i = 0;
    PyObject *key;
    PyObject *value;
    
    while (PyDict_Next(self, &i, &key, &value)) {
      PyDict_SetItem(new, key, value);  // shallow copy!
    }
    return new;
}

// shallow copy
static PyObject *
defdict_deepcopy(defdictobject *self, PyObject *args)
{
  // copy of defdict
    PyObject *new = PyObject_CallFunctionObjArgs((PyObject*)Py_TYPE(self),
						 self->default_factory, NULL, NULL);

    Py_ssize_t i = 0;
    PyObject *key;
    PyObject *value, *newvalue;
    
    while (PyDict_Next(self, &i, &key, &value)) {
      newvalue = new_mydouble(((mydouble *)value)->value); // deepcopy!
      PyDict_SetItem(new, key, newvalue);  
      Py_DECREF(newvalue);
    }
    return new;
}

static PyObject *
defdict_reduce(defdictobject *dd)
{
    /* __reduce__ must return a 5-tuple as follows:

       - factory function
       - tuple of args for the factory function
       - additional state (here None)
       - sequence iterator (here None)
       - dictionary iterator (yielding successive (key, value) pairs

       This API is used by pickle.py and copy.py.

       For this to be useful with pickle.py, the default_factory
       must be picklable; e.g., None, a built-in, or a global
       function in a module or package.

       Both shallow and deep copying are supported, but for deep
       copying, the default_factory must be deep-copyable; e.g. None,
       or a built-in (functions are not copyable at this time).

       This only works for subclasses as long as their constructor
       signature is compatible; the first argument must be the
       optional default_factory, defaulting to None.
    */
    PyObject *args;
    PyObject *items;
    PyObject *result;
    if (dd->default_factory == NULL || dd->default_factory == Py_None)
        args = PyTuple_New(0);
    else
        args = PyTuple_Pack(1, dd->default_factory);
    if (args == NULL)
        return NULL;
    items = PyObject_CallMethod((PyObject *)dd, "iteritems", "()");
    if (items == NULL) {
        Py_DECREF(args);
        return NULL;
    }
    result = PyTuple_Pack(5, Py_TYPE(dd), args,
                          Py_None, Py_None, items);
    Py_DECREF(items);
    Py_DECREF(args);
    return result;
}

/* Set a key error with the specified argument, wrapping it in a
 * tuple automatically so that tuple keys are not unpacked as the
 * exception arguments. */
static void
set_key_error(PyObject *arg)
{
    PyObject *tup;
    tup = PyTuple_Pack(1, arg);
    if (!tup)
        return; /* caller will expect error to be set anyway */
    PyErr_SetObject(PyExc_KeyError, tup);
    Py_DECREF(tup);
}

// for internal use
static mydouble *
_defdict_get(defdictobject *mp, register PyObject *key)
{
    PyObject *v;
    long hash;
    PyDictEntry *ep;
    assert(mp->ma_table != NULL);
    if (!PyString_CheckExact(key) ||
        (hash = ((PyStringObject *) key)->ob_shash) == -1) {
        hash = PyObject_Hash(key);
        if (hash == -1)
            return NULL;
    }
    ep = (mp->dict.ma_lookup)(mp, key, hash); // lhuang: subclassing; see dictobject.h
    if (ep == NULL)
        return NULL;
    v = ep->me_value;
    if (v == NULL) {
        if (!PyDict_CheckExact(mp)) {
          /* Look up __missing__ method if we're a subclass. */
          v = defdict_missing_add(mp, key);
	  Py_DECREF(v); // maintain ref count balance
	  return v;
        }
        set_key_error(key);
        return NULL;
    }
    return v;
}

// for external use
static PyObject *
defdict_get(defdictobject *mp, register PyObject *key) {

  mydouble *v = _defdict_get(mp, key);
  Py_INCREF(v);
  return v;
}

// TODO: keyword: step=...
static PyObject *
defdict_iaddi(defdictobject *self, PyObject *args)
{
    Py_ssize_t i = 0;
    PyObject *key;
    PyObject *value;
    //    PyObject *obj_self = (PyObject *)self;

    mydouble *item;
    double v;
    double c = self->step_c;
    PyObject *other;
    PyArg_ParseTuple(args, "O|d", &other, &c);  // c is step in avg
    
    while (PyDict_Next(other, &i, &key, &value)) {
      // in case of missing, added
      item = _defdict_get(self, key);
      v = ((mydouble *)value)->value;
      item->value += v;
      // new: avg perceptron
      item->second += v * c; 
    }
    Py_RETURN_NONE; // "void" type function
}  

// mydouble
static PyObject *
defdict_iadd(defdictobject *self, PyObject *other)
{
  PyObject *tup = PyTuple_Pack(1, other);
  defdict_iaddi(self, tup); // self.iadd(other, ...)
  Py_DECREF(tup);
  Py_INCREF(self); // only needed if calling +=
  return self;   // dunno why; but can't return self or 0  
}

static PyObject *
defdict_set_avg(defdictobject *self, PyObject *arg)
{
  Py_ssize_t i = 0;
  PyObject *key;
  PyObject *value;  
  mydouble *item;
  double x, y;
  double c = self->step_c; //default value
  if (!PyArg_Parse(arg, "d", &c))
    return NULL;

  if (c > 0) { // floating point
    // formula: avg = w - aw / c
    c = -1. / c; // N.B. -1. !!
    
    while (PyDict_Next(self, &i, &key, &value)) {
      item = (mydouble *)value;
      y = item->value;
      x = y + item->second * c;
      item->value = x; // now first value is avg value!
      item->second = y; // store old first value so that we can infer old second value
    }
  }
  Py_RETURN_NONE;  
}

static PyObject *
defdict_reset_avg(defdictobject *self, PyObject *arg)
{
  Py_ssize_t i = 0;
  PyObject *key;
  PyObject *value;  
  mydouble *item;
  double x, y;

  double c = self->step_c; // defaultvalue
  PyArg_Parse(arg, "d", &c);
  //c = PyFloat_AsDouble(arg);

  // formula: avg = w - aw / c
  // reverse:  aw = c * (w - a);  now: first is a, second is w

  while (PyDict_Next(self, &i, &key, &value)) {
    item = (mydouble *)value;
    y = item->second;
    item->second = c * (item->second - item->value);
    item->value = y;
  }
  Py_RETURN_NONE;  
}

static PyObject *
defdict_step(defdictobject *self, PyObject *args)
{
  double s = 1;
  PyArg_ParseTuple(args, "|d", &s);
  self->step_c += s;
  Py_RETURN_NONE;  
}

static PyObject *
defdict_set_step(defdictobject *self, PyObject *args)
{
  double s = 0;
  if (!PyArg_Parse(args, "d", &s))
    return NULL;
  self->step_c = s;
  Py_RETURN_NONE;  
}

static PyObject *
defdict_get_step(defdictobject *self)
{
  return PyFloat_FromDouble(self->step_c);
}

// mydouble 
// TODO: merge with iaddc
static PyObject *
defdict_iaddci(defdictobject *self, PyObject *args)
{
    Py_ssize_t i = 0;
    PyObject *key;
    PyObject *value;

    PyObject *other;
    double c_value = 1;
    double c = self->step_c;

    PyArg_ParseTuple(args, "O|d", &other, &c_value); // defdictobject, float -- note that O doesn't work in case of int!

    mydouble *item, *item2;

    while (PyDict_Next(other, &i, &key, &value)) {
      // in case of missing, added
      item2 = ((mydouble *)value);
      item = _defdict_get(self, key);
      item->value += item2->value * c_value;
      item->second += item2->second * c_value;      
    }
    Py_RETURN_NONE; // "void" type function
}  
    
static double
defdict_getdouble(defdictobject *mp, register PyObject *key)
{
    PyObject *v;
    long hash;
    PyDictEntry *ep;
    assert(mp->ma_table != NULL);
    if (!PyString_CheckExact(key) ||
        (hash = ((PyStringObject *) key)->ob_shash) == -1) {
        hash = PyObject_Hash(key);
        if (hash == -1)
          return 0; // dangerous
    }
    ep = (mp->dict.ma_lookup)(mp, key, hash); // lhuang: subclassing; see dictobject.h
    if (ep == NULL)
        return 0; // dangerous
    v = ep->me_value;
    if (v == NULL) {
      return 0; // missing, no add
    }
    return ((mydouble *)v)->value; // returns double
}

// return a python float instead of mydouble
static PyObject * 
defdict_subscript(defdictobject *mp, register PyObject *key) {
  return PyFloat_FromDouble(defdict_getdouble(mp, key)); // return python float
}

// called by PyObject_SetItem()
static int
defdict_setitem(defdictobject *self, PyObject *key, PyObject *value) {
  // TODO: check type first, if already mydouble, do not create new value
  // CAUTION: only the new value is inserted to the dict, not the value that comes in!
  // CAUTION: to insert your value, always use PyDict_SetItem, not PyObject_SetItem (which calls this func)!
  // CAUTION: see also. defdict_missing_add 

  // DONE: fix refcount
  PyObject *newvalue;
  // don't make a new mydouble if already the case
  if (Py_TYPE(value) != mydouble_type)
    // make a deepcopy by calling mydouble(value)
    newvalue = PyObject_CallFunctionObjArgs(self->default_factory, value, NULL);
  else 
    newvalue = value; // shallow copy!
    
  PyObject *result = PyDict_SetItem(self, key, newvalue);

  if (newvalue != value)
    Py_DECREF(newvalue);
  return result;
}

// assignment: d["a"] = 1 ==> will insert a mydouble type
// or delete : del d["a"] ==> will also free mydouble
static int
defdict_ass_sub(defdictobject *self, PyObject *key, PyObject *value) {
    if (value == NULL)
      return PyDict_DelItem((PyObject *)self, key);
    else
      return defdict_setitem(self, key, value);
}

static PyObject *
defdict_evaluate(defdictobject *self, PyListObject *other)
{
    Py_ssize_t i = 0;
    PyObject *obj_self = (PyObject *)self;
    
    double sum = 0;

    for (i = Py_SIZE(other); --i >= 0;) {
      sum += defdict_getdouble(obj_self, other->ob_item[i]);
    }

    return PyFloat_FromDouble(sum);
}  

static double dot(defdictobject *self, defdictobject *other)
{
  Py_ssize_t i = 0, len_self, len_other;
  PyObject *key;
  PyObject *value;

  double sum = 0;

  while (PyDict_Next(self, &i, &key, &value)) {
    sum += ((mydouble *)value)->value * defdict_getdouble(other, key);
  }
  return sum;
}

static PyObject *
defdict_dot(defdictobject *self, defdictobject *other)
{
    double sum = 0;
    
    Py_ssize_t len_self = PyObject_Size(self);
    Py_ssize_t len_other = PyObject_Size(other);

    sum = len_self < len_other ? dot(self, other) : dot(other, self);
    //    sum = dot(self, other);

    return PyFloat_FromDouble(sum);
}  

static PyObject *
defdict_iaddl(defdictobject *self, PyObject *args)
{
    Py_ssize_t i = 0;
    PyListObject *other;
    double c_value = 1; //default
    mydouble *item;
    
    PyArg_ParseTuple(args, "O|d", &other, &c_value); // defdictobject, float -- note that O doesn't work in case of int!

    for (i = Py_SIZE(other); --i >= 0;) {
      
      // in case of missing, added
      item = _defdict_get(self, other->ob_item[i]);
      item->value += c_value;
    }

    Py_RETURN_NONE;
}  

// lhuang: return a + b*c; new copy.
static PyObject *
defdict_avg(defdictobject *self, PyObject *args) {

    Py_ssize_t i = 0;
    PyObject *key;
    PyObject *value;
    mydouble *newvalue;

    PyObject *other;
    double c_value = 1;
    if (!PyArg_ParseTuple(args, "O|d", &other, &c_value))
      return NULL; // defdictobject, float -- note that O doesn't work in case of int!

    PyObject *new = PyObject_CallFunctionObjArgs((PyObject*)Py_TYPE(self),
                                                 self->default_factory, NULL, NULL);

    while (PyDict_Next(self, &i, &key, &value)) {

      //      newvalue = (mydouble *)(Py_TYPE(value)->tp_alloc(Py_TYPE(value), 0));
      newvalue = new_mydouble(((mydouble *)value)->value);//defdict_missing();
      newvalue->value += defdict_getdouble(other, key) * c_value;

      PyDict_SetItem(new, key, newvalue);

      Py_DECREF(newvalue); // important
    }

    return new;    
}

      // this is just like python calls, use NULL to terminate the list of 
      //      newvalue = PyObject_CallMethod(value, "copy", NULL); // deep copy
      //newvalue = PyObject_CallMethodObjArgs(value, copy_method, NULL); // deep copy
      //            newvalue = PyObject_CallFunctionObjArgs(mydouble_type, value, NULL); // deep copy
      // ImportError: symbol not found
	//	newvalue = (mydouble *)mydouble_copy((mydouble *)value);

/*       if (!ptype) */
/* 	ptype = Py_TYPE(value); */
//      newvalue = (mydouble *)PyEval_CallObject(self->default_factory, NULL);


// lhuang: add new methods here!
// note diff b/w deepcopy and __deepcopy__ (METH_NOARGS vs METH_O)
// the latter is for copy.deepcopy(...) which calls deepcopy with another argument
static PyMethodDef defdict_methods[] = {
    {"__getitem__", (PyCFunction)defdict_subscript,  METH_O | METH_COEXIST},
    {"__setitem__", (PyCFunction)defdict_setitem,  METH_VARARGS},
    {"copy", (PyCFunction)defdict_copy, METH_NOARGS, "shallow copy"},
    {"__copy__", (PyCFunction)defdict_copy, METH_NOARGS, "shallow_copy"},
    {"deepcopy", (PyCFunction)defdict_deepcopy, METH_NOARGS, "deep copy"},
    {"__deepcopy__", (PyCFunction)defdict_deepcopy, METH_O, "deep_copy"},
    {"__reduce__", (PyCFunction)defdict_reduce, METH_NOARGS, "for pickling"},
    {"iadd", (PyCFunction)defdict_iaddi, METH_VARARGS, "inplace add, returns void"},
    {"__iadd__", (PyCFunction)defdict_iadd, METH_VARARGS, "inplace add, returns self"},
    {"iaddc", (PyCFunction)defdict_iaddci, METH_VARARGS, "inplace add with rate"},
    {"evaluate", (PyCFunction)defdict_evaluate, METH_O, "dot-product with list"},
    {"dot", (PyCFunction)defdict_dot, METH_O, "dot-product"},
    {"get", (PyCFunction)defdict_get, METH_O, "returns mydouble"},
    {"iaddl", (PyCFunction)defdict_iaddl, METH_VARARGS, "inplace add with list"},
    {"addc", (PyCFunction)defdict_avg, METH_VARARGS, "add with rate (return new)"},
    {"__missing_add__", (PyCFunction)defdict_missing_add, METH_O, "default element"},
    {"set_avg", (PyCFunction)defdict_set_avg, METH_O, "compute and set avg weights"},
    {"reset_avg", (PyCFunction)defdict_reset_avg, METH_O, "restore old (non-avg) weights"},
    {"step", (PyCFunction)defdict_step, METH_VARARGS, "increase step count (for avg perceptron)"},
    {"get_step", (PyCFunction)defdict_get_step, METH_NOARGS, "get step"},
    {"set_step", (PyCFunction)defdict_set_step, METH_O, "set step"},
    {NULL}
};

static PyMemberDef defdict_members[] = {
    {"default_factory", T_OBJECT,
     offsetof(defdictobject, default_factory), 0,
     "Factory for default value called by __missing__()."},
    {NULL}
};

static void
defdict_dealloc(defdictobject *dd)
{
    Py_CLEAR(dd->default_factory);
    PyDict_Type.tp_dealloc((PyObject *)dd);
}

static int
defdict_print(defdictobject *dd, FILE *fp, int flags)
{
    int sts;
    Py_BEGIN_ALLOW_THREADS
    fprintf(fp, "mydefaultdict(");
    Py_END_ALLOW_THREADS
    if (dd->default_factory == NULL) {
        Py_BEGIN_ALLOW_THREADS
        fprintf(fp, "None");
        Py_END_ALLOW_THREADS
    } else {
        PyObject_Print(dd->default_factory, fp, 0);
    }
    Py_BEGIN_ALLOW_THREADS
    fprintf(fp, ", ");
    Py_END_ALLOW_THREADS
    sts = PyDict_Type.tp_print((PyObject *)dd, fp, 0);
    Py_BEGIN_ALLOW_THREADS
    fprintf(fp, ")");
    Py_END_ALLOW_THREADS
    return sts;
}

static PyObject *
defdict_repr(defdictobject *dd)
{
    PyObject *defrepr;
    PyObject *baserepr;
    PyObject *result;
    baserepr = PyDict_Type.tp_repr((PyObject *)dd);
    if (baserepr == NULL)
        return NULL;
    if (dd->default_factory == NULL)
        defrepr = PyString_FromString("None");
    else
    {
        int status = Py_ReprEnter(dd->default_factory);
        if (status != 0) {
            if (status < 0)
                return NULL;
            defrepr = PyString_FromString("...");
        }
        else
            defrepr = PyObject_Repr(dd->default_factory);
        Py_ReprLeave(dd->default_factory);
    }
    if (defrepr == NULL) {
        Py_DECREF(baserepr);
        return NULL;
    }
    result = PyString_FromFormat("mydefaultdict(%s, %s)",
                                 PyString_AS_STRING(defrepr),
                                 PyString_AS_STRING(baserepr));
    Py_DECREF(defrepr);
    Py_DECREF(baserepr);
    return result;
}

static int
defdict_traverse(PyObject *self, visitproc visit, void *arg)
{
    Py_VISIT(((defdictobject *)self)->default_factory);
    return PyDict_Type.tp_traverse(self, visit, arg);
}

static int
defdict_tp_clear(defdictobject *dd)
{
    Py_CLEAR(dd->default_factory);
    return PyDict_Type.tp_clear((PyObject *)dd);
}

static int
defdict_init(PyObject *self, PyObject *args, PyObject *kwds)
{
    defdictobject *dd = (defdictobject *)self;
    PyObject *olddefault = dd->default_factory;
    PyObject *newdefault = NULL;
    PyObject *newargs;
    double step = 0;
    int result;
    if (args == NULL || !PyTuple_Check(args))
        newargs = PyTuple_New(0);
    else {
        Py_ssize_t n = PyTuple_GET_SIZE(args);
        if (n > 0) {
            newdefault = PyTuple_GET_ITEM(args, 0);
            if (!PyCallable_Check(newdefault) && newdefault != Py_None) {
                PyErr_SetString(PyExc_TypeError,
                    "first argument must be callable");
                return -1;
            }
            newargs = PySequence_GetSlice(args, 1, n);
        }
    }
    if (newargs == NULL)
        return -1;
    Py_XINCREF(newdefault);
    dd->default_factory = newdefault;
    result = PyDict_Type.tp_init(self, newargs, kwds); // call superclass init for other arguments
    dd->step_c = step;
    Py_DECREF(newargs);
    Py_XDECREF(olddefault);

    // global
    if (!mydouble_type) // do it only once
      mydouble_type = Py_TYPE(PyEval_CallObject(dd->default_factory, NULL));

    return result;
}

PyDoc_STRVAR(defdict_doc,
"defaultdict(default_factory) --> dict with default factory\n\
\n\
The default factory is called without arguments to produce\n\
a new value when a key is not present, in __getitem__ only.\n\
A defaultdict compares equal to a dict with the same items.\n\
");

/* See comment in xxsubtype.c */
#define DEFERRED_ADDRESS(ADDR) 0

// lhuang: so that += calls __iadd__
static PySequenceMethods defdict_as_sequence = {
    0,                       /* sq_length */
    0,                    /* sq_concat */
    0,                  /* sq_repeat */
    0,                    /* sq_item */
    0,              /* sq_slice */
    0,             /* sq_ass_item */
    0,       /* sq_ass_slice */
    0,                  /* sq_contains */
    (binaryfunc)defdict_iadd,            /* sq_inplace_concat */
    0,          /* sq_inplace_repeat */
};

static PyMappingMethods defdict_as_mapping = {
    0, /*mp_length*/
    (binaryfunc)defdict_subscript, /*mp_subscript (getitem) */
    (objobjargproc)defdict_ass_sub, /*mp_ass_subscript (setitem) */
};

static PyTypeObject defdict_type = {
    PyVarObject_HEAD_INIT(DEFERRED_ADDRESS(&PyType_Type), 0)
    "mydefaultdict",                    /* tp_name */
    sizeof(defdictobject),              /* tp_basicsize */
    0,                                  /* tp_itemsize */
    /* methods */
    (destructor)defdict_dealloc,        /* tp_dealloc */
    (printfunc)defdict_print,           /* tp_print */
    0,                                  /* tp_getattr */
    0,                                  /* tp_setattr */
    0,                                  /* tp_compare */
    (reprfunc)defdict_repr,             /* tp_repr */
    0,                 /* tp_as_number */
    &defdict_as_sequence,                /* tp_as_sequence */
    &defdict_as_mapping,                 /* tp_as_mapping */
    0,                                  /* tp_hash */
    0,                                  /* tp_call */
    0,                                  /* tp_str */
    PyObject_GenericGetAttr,            /* tp_getattro */
    0,                                  /* tp_setattro */
    0,                                  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC |
        Py_TPFLAGS_HAVE_WEAKREFS,               /* tp_flags */
    defdict_doc,                        /* tp_doc */
    defdict_traverse,                   /* tp_traverse */
    (inquiry)defdict_tp_clear,          /* tp_clear */
    0,                                  /* tp_richcompare */
    0,                                  /* tp_weaklistoffset*/
    0,                                  /* tp_iter */
    0,                                  /* tp_iternext */
    defdict_methods,                    /* tp_methods */
    defdict_members,                    /* tp_members */
    0,                                  /* tp_getset */
    DEFERRED_ADDRESS(&PyDict_Type),     /* tp_base */
    0,                                  /* tp_dict */
    0,                                  /* tp_descr_get */
    0,                                  /* tp_descr_set */
    0,                                  /* tp_dictoffset */
    defdict_init,                       /* tp_init */
    PyType_GenericAlloc,                /* tp_alloc */
    0,                                  /* tp_new */
    PyObject_GC_Del,                    /* tp_free */
};

/* module level code ********************************************************/

PyDoc_STRVAR(module_doc,
"High performance data structures.\n\
- mydefaultdict:  my dict subclass with a default value factory\n\
");

PyMethodDef methods[] = {
    {NULL}
};

PyMODINIT_FUNC
init_mycollections(void)
{
    PyObject *m;

    m = Py_InitModule3("_mycollections", methods, module_doc);
    if (m == NULL)
        return;
    
    defdict_type.tp_base = &PyDict_Type;
    if (PyType_Ready(&defdict_type) < 0)
        return;
    Py_INCREF(&defdict_type);
    PyModule_AddObject(m, "mydefaultdict", (PyObject *)&defdict_type);

    return;
}
