#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "./include/metrics.h"
#include "./include/algorithms.h"


static PyObject *method_route_cost(PyObject *self, PyObject *args) {
    PyObject *cost_matrix;
    PyObject *route;
    int n;

    if (!PyArg_ParseTuple(args, "OOi", &cost_matrix, &route, &n)) {
        return NULL;
    }

    float **cost_matrix_2d = (float **)malloc(n * sizeof(float *));
    for (int i = 0; i < n; i++) {
        cost_matrix_2d[i] = (float *)malloc(n * sizeof(float));
    }

    for (int i = 0; i < n; i++) {
        PyObject *row = PyList_GetItem(cost_matrix, i);
        for (int j = 0; j < n; j++) {
            PyObject *item = PyList_GetItem(row, j);
            cost_matrix_2d[i][j] = PyFloat_AsDouble(item);
            if (PyErr_Occurred()) {
                PyErr_SetString(PyExc_TypeError, "Cost matrix must be a list of lists of numbers.");
                return NULL;
            }
        }
    }

    int *route_1d = (int *)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) {
        PyObject *item = PyList_GetItem(route, i);
        route_1d[i] = PyLong_AsLong(item);
        if (PyErr_Occurred()) {
            PyErr_SetString(PyExc_TypeError, "Route must be a list of integers.");
            return NULL;
        }
    }

    float cost = route_cost(cost_matrix_2d, route_1d, n);

    return Py_BuildValue("f", cost);
}


// Wrap the nearest neighbor algorithm in a python function
static PyObject *method_nearest_neighbors(PyObject *self, PyObject *args) {

    /* Parse arguments */
    PyObject *cost_matrix;
    PyObject *row_cost_matrix;
    PyObject *cost;
    Py_ssize_t n;
    int i, j;

    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &cost_matrix)) {
        PyErr_SetString(PyExc_TypeError, "parameter must be a list.");
        return NULL;
    }
    n = PyList_Size(cost_matrix);

    // Read a list of list of floats
    float **cost_matrix_c = (float **)malloc(n * sizeof(float *));
    for (i = 0; i < n; i++) {
        row_cost_matrix = PyList_GetItem(cost_matrix, i);
        cost_matrix_c[i] = (float *)malloc(n * sizeof(float));
        for (j = 0; j < n; j++) {
            cost = PyList_GetItem(row_cost_matrix, j);
            cost_matrix_c[i][j] = PyFloat_AsDouble(cost);
            if (PyErr_Occurred()) {
                PyErr_SetString(PyExc_TypeError, "Cost matrix must be a list of lists of numbers.");
                return NULL;
            }
        }
    }

    /* Call the C function */
    int *route = nearest_neighbors(cost_matrix_c, n);

    /* Convert the C array to a Python list */
    PyObject *py_route = PyList_New(n);
    for (i=0; i<n; i++) {
        PyList_SetItem(py_route, i, PyLong_FromLong(route[i]));
    }

    return py_route;
};


// Wrap the two opt algorithm in a python function
static PyObject *method_two_opt(PyObject *self, PyObject *args) {

    /* Parse arguments */
    PyObject *cost_matrix;
    PyObject *row_cost_matrix;
    PyObject *cost;
    PyObject *route;
    PyObject *node;
    Py_ssize_t n, cost_n;
    int i, j;

    if (!PyArg_ParseTuple(args, "O!O!", &PyList_Type, &cost_matrix, &PyList_Type, &route)) {
        PyErr_SetString(PyExc_TypeError, "parameters must be lists.");
        return NULL;
    }
    cost_n = PyList_Size(cost_matrix);
    n = PyList_Size(route);

    // Read a list of list of floats
    float **cost_matrix_c = (float **)malloc(cost_n * sizeof(float *));
    for (i = 0; i < cost_n; i++) {
        row_cost_matrix = PyList_GetItem(cost_matrix, i);
        cost_matrix_c[i] = (float *)malloc(cost_n * sizeof(float));
        for (j = 0; j < cost_n; j++) {
            cost = PyList_GetItem(row_cost_matrix, j);
            cost_matrix_c[i][j] = PyFloat_AsDouble(cost);
            if (PyErr_Occurred()) {
                PyErr_SetString(PyExc_TypeError, "Cost matrix must be a list of lists of numbers.");
                return NULL;
            }
        }
    }

    // Read a list of integers
    int *route_c = (int *)malloc(n * sizeof(int));
    for (i = 0; i < n; i++) {
        node = PyList_GetItem(route, i);
        route_c[i] = PyLong_AsLong(node);
        if (PyErr_Occurred()) {
            PyErr_SetString(PyExc_TypeError, "Route must be a list of integers.");
            return NULL;
        }
    }

    /* Call the C function */
    int *new_route = two_opt(cost_matrix_c, route_c, n);

    /* Convert the C array to a Python list */
    PyObject *py_route = PyList_New(n);
    for (i=0; i<n; i++) {
        PyList_SetItem(py_route, i, PyLong_FromLong(new_route[i]));
    }

    return py_route;
};



static PyMethodDef TSPMethods[] = {
    {"nn", method_nearest_neighbors, METH_VARARGS, "Python interface for calculating Nearest Neighbours solution to the TSP problem"},
    {"route_cost", method_route_cost, METH_VARARGS, "Python interface for calculating the cost of a route"},
    {"two_opt", method_two_opt, METH_VARARGS, "Python interface for calculating the 2-opt solution to the TSP problem"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef tspmodule = {
    PyModuleDef_HEAD_INIT,
    "ctsp",
    "Python interface for calculating TSP solutions as a C library function",
    -1,
    TSPMethods
};

PyMODINIT_FUNC PyInit_ctsp(void) {
    return PyModule_Create(&tspmodule);
}