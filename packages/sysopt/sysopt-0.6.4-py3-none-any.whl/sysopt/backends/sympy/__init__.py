"""Sympy backend. Allows rendering of system models to symbolic equations."""

import numpy as np
import sympy as sp
import sympy.core
from sysopt.backends.sympy.math import *
import sysopt.backends.sympy.expression_graph
from sysopt.backends.sympy.integrator import get_integrator


def sparse_matrix(shape):
    return sp.MutableSparseMatrix(*shape, {})


def list_symbols(expr) -> set:
    return {a for a in expr.atoms() if isinstance(a, sympy.core.Symbol)}


def as_array(item):
    return np.array(item, dtype=float)
