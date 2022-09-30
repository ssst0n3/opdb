#include "Python.h"
#include "frameobject.h"

#define PyFrame_Check(op) ((op)->ob_type == &PyFrame_Type)

static PyObject* getStackSize(PyObject *self, PyObject *args)
{
	PyObject **stack_pointer;
	PyFrameObject* frame;

	if (!PyFrame_Check(args))
	{
		PyErr_SetString(PyExc_TypeError, "Arguement to getStackSize must be a frame object.");
		return NULL;
	}
	frame = (PyFrameObject*) args;
	stack_pointer = frame->f_stacktop;
	int stacksize = ((int)(stack_pointer - frame->f_valuestack));
	return PyLong_FromLong(stacksize);
}

static PyObject* getStackItem(PyObject *self, PyObject *args)
{
	PyFrameObject* frame;
	PyObject **stack_pointer;
	int itemindex;
    if (!PyArg_ParseTuple(args, "Oi", &frame, &itemindex))
	{
		PyErr_SetString(PyExc_TypeError, "Argument to getStackItem must be frame object and an integer index.");
        return NULL;
	}
	stack_pointer = frame->f_stacktop;
	if (stack_pointer == NULL) {
		PyErr_SetString(PyExc_TypeError, "frame does not exist");
        return NULL;
	}

	int stacksize = ((int)(stack_pointer - frame->f_valuestack));
    if (itemindex < 0 || itemindex >= stacksize )
	{
		PyErr_SetString(PyExc_TypeError, "Invalid index");
        return NULL;
//		Py_RETURN_NONE;
	}
	PyObject *ob = stack_pointer[-(itemindex+1)];
	if (ob) {
    	Py_INCREF(ob);
	} else {
		Py_RETURN_NONE;
	}
	return ob;
}


static PyMethodDef pystackMethods[] =
{
    {"getStackSize", getStackSize, METH_O, "Gets the stack size."},
	{"getStackItem", getStackItem, METH_VARARGS, "Gets the stack item at an index."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef pystack =
{
    PyModuleDef_HEAD_INIT,
    "pystack", /* name of module */
    "",          /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    pystackMethods
};

PyMODINIT_FUNC PyInit_pystack(void)
{
    return PyModule_Create(&pystack);
}