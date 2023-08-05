"""Functions and classes to for symbolic manipulation."""
import weakref
from abc import ABCMeta, abstractmethod
from collections import defaultdict
from inspect import signature

import numpy as np
from scipy.sparse import dok_matrix
import ordered_set
from typing import Union, List, Callable, Tuple, Optional, Dict, NewType, Any

from sysopt.helpers import flatten, slice_to_list
from sysopt.exceptions import InvalidShape, EvaluationError

array = np.array
epsilon = 1e-12

SymbolicArray = NewType('SymbolicArray',
                        Union[List['Variable'], Tuple['Variable']])


# ------------------------------------------------------------------------------
# ----------------------- Array Handling and Linear Algebra---------------------
# ------------------------------------------------------------------------------


class Matrix(np.ndarray):
    """View of a numpy matrix for use in expression graphs."""

    def __hash__(self):
        shape_hash = hash(self.shape)
        data_hash = hash(tuple(self.ravel()))
        return hash((shape_hash, data_hash))

    def __cmp__(self, other):
        return self is other

    def __eq__(self, other):
        if isinstance(other, (list, tuple)):
            return other == self.tolist()

        if isinstance(other, (float, int, complex)):
            if self.shape == (1,):
                return self[0] == other
            elif self.shape == (1, 1):
                return self[0, 0] == other
            return False

        try:
            if self.shape != other.shape:
                return False
        except AttributeError:
            return False
        if hash(self) != hash(other):
            return False
        result = (self - other) == 0
        if isinstance(result, np.ndarray):
            return result.all()
        else:
            return result


class SparseMatrix(dok_matrix):
    """Dictionary-of-keys sparse matrix."""

    def __eq__(self, other):

        try:
            if self.shape != other.shape:
                return False
            if set(self.keys()) != set(other.keys()):
                return False
        except AttributeError:
            return False

        return all(other[key] == value for key, value in self.items())

    def __hash__(self):
        return hash((self.shape, tuple(self.items())))

    def ravel(self):
        return self.todense().view(Matrix).ravel()

    @property
    def T(self):  # pylint: disable=invalid-name

        m = SparseMatrix((self.shape[1], self.shape[0]))
        for (i, j), v in self.items():
            m[j, i] = v

        return m

    def __mul__(self, other):
        if isinstance(other, SparseMatrix):
            return super().__mul__(other)
        a = self.todense().view(Matrix)
        out = a * other
        return out

    def __matmul__(self, other):

        if isinstance(other, SparseMatrix):
            r = super().__matmul__(other)
            return r
        elif isinstance(other, np.ndarray):
            out = (self.todense() @ other).view(Matrix)
            if len(other.shape) == 2:
                out = out.reshape((self.shape[0], other.shape[1]))
            else:
                out = out.reshape((self.shape[0], ))

            return out
        if isinstance(other, Algebraic):
            r = ExpressionGraph(matmul, self, other)

            return r
        assert False, f'Matmul not define for {other.__class__}'


def sparse_matrix(shape: Tuple[int, int]):
    """Create an empty sparse matrix of the given dimension.

    Todo:
        replace with an actual sparse matrix representaiton!

    """
    if len(shape) == 1:

        return np.zeros(shape, dtype=float).view(Matrix)

    return SparseMatrix(shape)


def basis_vector(index, dimension):
    """Get the corresponding standard Euclidian basis vector."""
    e_i = np.zeros(shape=(dimension,), dtype=float).view(Matrix)
    e_i[index] = 1
    return e_i


class LinearMap:
    """Functional representation of a linear operator defined by a matrix."""

    def __init__(self, matrix):
        self.matrix = matrix

    @property
    def T(self):    # pylint: disable=invalid-name
        return LinearMap(self.matrix.T.copy())

    def __call__(self, arg):
        return ExpressionGraph(matmul, self.matrix, arg)


def as_array(item: Union[List[Union[int, float]], int, float, np.ndarray],
             prototype: 'Variable' = None):

    if isinstance(item, Algebraic):
        return item
    if isinstance(item, np.ndarray):
        return item.view(Matrix)
    elif isinstance(item, dok_matrix):
        return item
    elif isinstance(item, (list, tuple)):
        return concatenate(*item)
    elif isinstance(item, (int, float)):
        m = np.array([item], dtype=float).view(Matrix)
        return m
    elif item is None:
        return None
    elif callable(item):
        return Function(prototype.shape, item, prototype)

    raise NotImplementedError(
        f'Don\'t know how to treat {item} of type {type(item)} as an array')


def inclusion_map(basis_map: Dict[int, int],
                  domain_dimension: int,
                  codomain_dimension: int):
    """Project the domain onto a subspace spanned by the indices.

    row space: dimension of the subspace
    col space: dimension of the source

    Args:
        basis_map:          Coordinate indices of the vector subspace.
        domain_dimension:   Dimension of the domain.
        codomain_dimension: Dimension of the codomain

    basis map should be of the form domain -> codomain

    """

    if domain_dimension == 1:
        if codomain_dimension == 1:
            return lambda x: ExpressionGraph(mul, 1, x)
        else:
            assert len(basis_map) == 1
            j = basis_map[0]
            e_j = basis_vector(j, codomain_dimension)
            return lambda x: ExpressionGraph(mul, e_j, x)

    matrix = sparse_matrix((codomain_dimension, domain_dimension))

    for i, j in basis_map.items():
        matrix[j, i] = 1
    return LinearMap(matrix)


def restriction_map(indices: Union[List[int], Dict[int, int]],
                    superset_dimension: int) -> Callable:

    if isinstance(indices, (list, tuple)):
        domain = len(indices)
        iterator = enumerate(indices)
    else:
        domain = max(indices.keys()) + 1
        iterator = indices.items()

    if domain == superset_dimension == 1:
        return lambda x: ExpressionGraph(mul, 1, x)

    matrix = sparse_matrix((domain, superset_dimension))
    for i, j in iterator:
        matrix[i, j] = 1

    return LinearMap(matrix)


def as_vector(arg):
    if isinstance(arg, Algebraic) or is_vector_like(arg):
        return arg
    if isinstance(arg, (list, tuple)):
        return flatten(arg, 1)

    if isinstance(arg, (int, float)):
        return [arg]

    if arg is None:
        return []

    raise NotImplementedError(
        f'Don\'t know to to vectorise {arg.__class__}'
    )


def concatenate(*arguments):
    length = 0
    scalar_constants = []
    vectors = []
    # put all scalar constants into a single vector
    # multiply all vector constants and vector graphs by inclusion maps
    if all(isinstance(a, np.ndarray) for a in arguments):
        return np.concatenate(arguments)

    for arg in arguments:
        if arg is None:
            continue
        if isinstance(arg, (int, float, complex)):
            scalar_constants.append((length, arg))
            length += 1
            continue
        assert len(arg.shape) == 1,\
            f'Cannot concatenate object with shape {arg.shape}'

        n, = arg.shape
        basis_map = dict(enumerate(range(length, length + n)))
        vectors.append((basis_map, n, arg))
        length = length + n

    result = sparse_matrix((length, ))
    while scalar_constants:
        i, v = scalar_constants.pop()
        result[i] = v

    while vectors:
        basis_map, domain, vector = vectors.pop()
        inclusion = inclusion_map(basis_map, domain, length)
        result = result + inclusion(vector)

    return result


# ------------------------------------------------------------------------------
# ------------------ Shape Operations ------------------------------------------
# ------------------------------------------------------------------------------
# When building an expression tree out of matrix/vector operations, we'd like
# to keep track of the shapes of the tree.
# Here is the magic that makes that happen!

__ops = defaultdict(list)
__shape_ops = {}
__op_strings = {}
scalar_shape = (1, )


def _infer_shape(op: Callable, *shapes: Tuple[int, ...]) -> Tuple[int, ...]:
    """Infers the output shape from the operation on the given inputs."""
    return __shape_ops[op](*shapes)


def _infer_scalar_shape(*shapes: Tuple[int, ...]) -> Tuple[int, ...]:
    this_shape = shapes[0]
    for shape in shapes[1:]:
        if shape in (this_shape, scalar_shape):
            continue
        if this_shape == (1, ):
            this_shape = shape
        else:
            raise InvalidShape('Invalid Shape')
    return this_shape


def matmul_shape(*shapes: Tuple[int, ...]) -> Tuple[int, ...]:
    n, m = shapes[0]
    for shape in shapes[1:]:
        try:
            n_next, m_next = shape
        except ValueError:
            n_next, = shape
            m_next = None
        if m != n_next:
            raise InvalidShape('Invalid shape')
        else:
            m = m_next

    if m is not None:
        return n, m
    else:
        return n,


def transpose_shape(shape: Tuple[int, int]) -> Tuple[int, ...]:
    """Computes the shape of the transposed matrix."""
    try:
        n, m = shape
    except ValueError:
        n, = shape
        m = 1
    return m, n


# ------------------------------------------------------------------------------
# ------------------ Graph Operations ------------------------------------------
# ------------------------------------------------------------------------------
# Here is the the methods that allow functions / operations to be stored in
# and expression graph


def register_op(shape_func=_infer_scalar_shape, string=None):
    """Decorator which register the operator as an expression graph op."""
    def wrapper(func):
        sig = signature(func)
        is_variable = any(
            param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD)
            for param in sig.parameters.values())

        idx = None if is_variable else len(sig.parameters)
        __ops[idx].append(func)
        __shape_ops[func] = shape_func
        if string:
            __op_strings[func] = string
        return func

    return wrapper


def op_to_string(op):
    try:
        return __op_strings[op]
    except KeyError:
        return str(op)


def wrap_ufunc(ufunc: Callable,
               arguments: Optional[int] = None,
               shape_func=_infer_scalar_shape,) -> Callable:
    """Wraps the function for use in expression graphs.

    Args:
        func:       A function to wrap
        arguments:  The number of arguments
        shape_func: A function which generates the output shape from the
            arguments.
        numpy_func: Numpy function which this wraps.

    Returns:
        An callable operator for use in an expression graph.

    """
    __ops[arguments].append(ufunc)

    def wrapper(*args):
        return ExpressionGraph(ufunc, *args)

    __shape_ops[ufunc] = shape_func

    decorator = implements(ufunc)

    return decorator(wrapper)


def is_op(value):
    try:
        return any(value in ops for ops in __ops.values())
    except ValueError:
        return False


def implements(numpy_function):
    """Register an __array_function__ implementation for MyArray objects."""
    def decorator(func):
        numpy_handlers[numpy_function] = func
        return func
    return decorator


@register_op(string='pow')
def power(base, exponent):
    return base ** exponent


@register_op(string='+')
def add(lhs, rhs):
    return lhs + rhs


@register_op(string='-')
def sub(lhs, rhs):
    return lhs - rhs


@register_op(shape_func=matmul_shape, string='@')
def matmul(lhs, rhs):
    if isinstance(lhs, (int, float)) or isinstance(rhs, (int, float)):
        return lhs * rhs
    return lhs @ rhs


@register_op(string='-')
def neg(obj):
    return -obj


@register_op(string='*')
def mul(lhs, rhs):
    return lhs * rhs


@register_op(string='/')
def div(lhs, rhs):
    return lhs / rhs


@register_op(shape_func=transpose_shape, string='transpose')
def transpose(matrix):
    return matrix.T


numpy_handlers = {
    np.matmul: lambda a, b: ExpressionGraph(matmul, a, b),
    np.multiply: lambda a, b: ExpressionGraph(mul, a, b),
    np.add: lambda a, b: ExpressionGraph(add, a, b),
    np.subtract: lambda a, b: ExpressionGraph(sub, a, b),
    np.divide: lambda a, b: ExpressionGraph(div, a, b),
    np.negative: lambda x: ExpressionGraph(neg, x),
    np.transpose: lambda x: ExpressionGraph(transpose, x),
    np.power: lambda a, b: ExpressionGraph(power, a, b),
    np.deg2rad: lambda x: ExpressionGraph(mul, np.pi/180, x),
    np.rad2deg: lambda x: ExpressionGraph(mul, 180/np.pi, x)
}

exp = wrap_ufunc(np.exp, 1)
log = wrap_ufunc(np.log, 1)
sin = wrap_ufunc(np.sin, 1)
cos = wrap_ufunc(np.cos, 1)
tan = wrap_ufunc(np.tan, 1)
asin = wrap_ufunc(np.arcsin, 1)
acos = wrap_ufunc(np.arccos, 1)
atan = wrap_ufunc(np.arctan, 1)
sinh = wrap_ufunc(np.sinh, 1)
cosh = wrap_ufunc(np.cosh, 1)
tanh = wrap_ufunc(np.tanh, 1)
asinh = wrap_ufunc(np.arcsinh, 1)
acosh = wrap_ufunc(np.arccosh, 1)
atanh = wrap_ufunc(np.arctanh, 1)
fabs = wrap_ufunc(np.abs, 1)


heaviside = wrap_ufunc(np.heaviside, 1)

sign = wrap_ufunc(np.sign, 1)
atan2 = wrap_ufunc(np.arctan2, 2)

unary = [
    sin, cos, asin, acos, tan, atan,
    sinh, asinh, cosh, acosh, tanh, atanh,
    exp, log, heaviside, sign
]

binary = [
    atan2   # add, subtract, multiply, divide
]

# ------------------------------------------------------------------------------
# ------------------     Graph Classes     -------------------------------------
# ------------------------------------------------------------------------------


class Algebraic(metaclass=ABCMeta):
    """Base class for symbolic terms in expression graphs."""

    def __len__(self):
        if len(self.shape) == 1:
            return self.shape[0]

        raise ValueError('Cannot determine the length of a non-vector object')

    def __array_ufunc__(self, func, method, *args, **kwargs):
        if func not in numpy_handlers:
            return NotImplemented
        if method != '__call__':
            return NotImplemented
        return numpy_handlers[func](*args, **kwargs)

    def __array_function__(self, func, types, args, kwargs):
        if func not in numpy_handlers:
            return NotImplemented
        return numpy_handlers[func](*args, **kwargs)

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError(
            f'{str(self.__class__)} is missing this method'
        )

    @property
    @abstractmethod
    def shape(self):
        raise NotImplementedError

    @property
    def T(self):  # pylint: disable=invalid-name
        return ExpressionGraph(transpose, self)

    @abstractmethod
    def symbols(self):
        raise NotImplementedError

    @abstractmethod
    def __hash__(self):
        raise NotImplementedError

    def __getitem__(self, item):
        n = self.shape[0]
        if isinstance(item, slice):
            indices = slice_to_list(item, n)
        else:
            indices = [item]

        if indices == [range(n)]:
            return self

        pi = restriction_map(indices, n)
        return pi(self)

    def __iter__(self):
        n = self.shape[0]
        for i in range(n):
            yield restriction_map([i], n)(self)

    def __add__(self, other):
        if is_zero(other, self.shape):
            return self

        return ExpressionGraph(add, self, other)

    def __radd__(self, other):
        if is_zero(other, self.shape):
            return self
        return ExpressionGraph(add, other, self)

    def __neg__(self):
        return ExpressionGraph(neg, self)

    def __sub__(self, other):
        return ExpressionGraph(sub, self, other)

    def __rsub__(self, other):
        return ExpressionGraph(sub, other, self)

    def __matmul__(self, other):
        return ExpressionGraph(matmul, self, other)

    def __rmatmul__(self, other):
        return ExpressionGraph(matmul, other, self)

    def __mul__(self, other):
        return ExpressionGraph(mul, self, other)

    def __rmul__(self, other):
        return ExpressionGraph(mul, other, self)

    def __truediv__(self, other):
        return ExpressionGraph(div, self, other)

    def __rtruediv__(self, other):
        return ExpressionGraph(div, other, self)

    def __le__(self, other):
        return _less_or_equal(self, other)

    def __ge__(self, other):
        return _less_or_equal(other, self)

    def __gt__(self, other):
        return _less_or_equal(other, self + epsilon)

    def __lt__(self, other):
        return _less_or_equal(self, other + epsilon)

    def __cmp__(self, other):
        return id(self) == id(other)

    def __pow__(self, exponent, modulo=None):
        return ExpressionGraph(power, self, exponent)


def _less_or_equal(smaller, bigger):
    if is_temporal(smaller) or is_temporal(bigger):
        return PathInequality(smaller, bigger)
    else:
        return Inequality(smaller, bigger)


class Variable(Algebraic):
    """Symbolic type for a free variable."""
    is_symbolic = True
    __array_ufunc__ = None

    def __init__(self, name=None, shape=scalar_shape):
        self._shape = (shape, ) if isinstance(shape, int) else shape
        self._name = name

    def __str__(self):
        shape_str = 'x'.join(str(n) for n in self.shape)
        return f'{self.name}^({shape_str})'

    def __repr__(self):
        if self.name is not None:
            return f'{self.__class__.__name__}({self.name}, {self.shape})'
        else:
            return 'unnamed_variable'

    @property
    def name(self):
        return self._name

    @property
    def shape(self):
        return self._shape

    def symbols(self):
        return {self}

    def __hash__(self):
        return hash(id(self))

    def __cmp__(self, other):
        return id(self) == id(other)


class Function(Algebraic):
    """Wrapper for function calls.

    Args:
        shape: Output shape of the function (only supports values of `(d,)`
            where `d` is the output range.
        function: The means of evaluating this function
        arguments: The arguments to for this function

    Keyword Args:
        jacobian: Function that takes `arguments` and produces a list
            of jacobians with respect to the given arguments
        forwards: Function that takes the `arguments` and rates of change
            for each argument, and produces the corresponding rate of change
            of the function.

    """

    def __init__(self,
                 shape: Tuple[int],
                 function: Callable,
                 arguments: List[SymbolicArray],
                 jacobian: Optional[Callable] = None,
                 forwards: Optional[Callable] = None,
                 ):
        self._shape = shape
        self.function = function
        self.arguments = tuple(arguments)
        self.jacobian = jacobian
        self.forwards = forwards

    def __repr__(self):
        args = ','.join(str(a) for a in self.arguments)
        return f'{str(self.function)}({args})'

    @property
    def shape(self):
        return self._shape

    def __hash__(self):
        return hash((id(self.function), id(self.jacobian), self.arguments))

    def symbols(self):
        return set(self.arguments)

    def __call__(self, *args):
        assert len(args) == len(self.arguments)
        if any(is_symbolic(arg) for arg in args):
            return Composition(self, dict(zip(self.arguments, args)))

        return self.function(*args)

    def call(self, args_dict):
        args = [args_dict[arg] for arg in self.arguments]
        result = self(*args)
        return result


class Composition(Algebraic):
    """Composition of a function with other functions/graphs

    Args:
        function: The function to be called symbolically
        arguments: dictionary of symbolic call where the keys identify
            the arguments of the function, and the values identify the
            assigned (possibly symbolic) values.

    """

    def __init__(self, function: Function, arguments: Dict['Variable', Any]):
        self.function = function
        self.arg_map = arguments
        self.arguments = ordered_set.OrderedSet()

        for arg in arguments.values():
            try:
                self.arguments.update(arg.symbols())
            except AttributeError:
                pass

    def symbols(self):
        return self.arguments

    @property
    def shape(self):
        return self.function.shape

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return f'Closure {self.function}({self.arg_map})'

    def __call__(self, *args):
        assert len(args) == len(self.arguments)
        return self.call(dict(zip(self.arguments, args)))

    def call(self, arg_dict: Dict[SymbolicArray, Any]):
        call_args = {}
        for inner_arg in self.function.arguments:
            arg = self.arg_map[inner_arg]
            if not is_symbolic(arg):
                call_args[inner_arg] = arg
            elif isinstance(arg, ExpressionGraph):
                call_args[inner_arg] = arg.call(arg_dict)
            else:
                call_args[inner_arg] = arg_dict[arg]
        return self.function.call(call_args)


class ExpressionGraph(Algebraic):
    """Graph representation of a symbolic expression."""

    def __init__(self, op, *args):
        self.nodes = []
        self.edges = defaultdict(list)
        self._head = None
        op_node = self.add_or_get_node(op)
        self.edges.update(
            {op_node: [self.add_or_get_node(a) for a in args]}
        )
        self._shape = None
        self.head = op_node

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, value):
        self._shape = self._get_shape_of(value)
        self._head = value

    @property
    def shape(self):
        return self._shape

    def _get_shape_of(self, node):

        if node in self.edges:
            op = self.nodes[node]
            shapes = [
                self._get_shape_of(child)
                for child in self.edges[node]
            ]
            return _infer_shape(op, *shapes)

        obj = self.nodes[node]
        try:
            return obj.shape
        except AttributeError:
            if isinstance(obj, (float, int, complex)):
                return scalar_shape
        raise NotImplementedError(
            f'Don\'t know how to get the shape of {obj}'
        )

    def __call__(self, *args, **kwargs):

        assert len(args) == len(self.symbols()),\
            f'Tried to call function with {self.symbols()} '
        values = dict(zip(self.symbols(), args))
        return self.call(values)

    def call(self, values: Union[List, Dict]) -> Union[Algebraic, np.ndarray]:
        """Call the graph with the given arguments.

        Args:
            values - A list or dictionary of arguments.

        Try to evaluate the graph with the given arguments.
        A partial call
        """
        invalid_args = {
            str(k): v for k, v in values.items() if v is None
        }
        if invalid_args:
            raise TypeError(f'Invalid arguments {invalid_args}')
        arguments = {
            k: as_array(v, prototype=k) for k, v in values.items()
        }

        context = {}
        sorted_nodes = self.get_topological_sorted_indices()

        def eval_node(obj):
            if is_op(obj):
                args = [context[child] for child in self.edges[node]]
                out = obj(*args)

                return out
            try:
                return obj.call(arguments)
            except (AttributeError, TypeError):
                pass
            try:
                return arguments[obj]
            except (KeyError, TypeError):
                pass
            return obj
        path = []
        while sorted_nodes:
            node = sorted_nodes.pop()
            path.append(node)
            if node in context:
                continue
            obj = self.nodes[node]
            try:
                context[node] = eval_node(obj)
            except Exception as ex:
                raise EvaluationError(self, context, path, ex) from ex
        result = context[self.head]
        try:
            # mostly for numpy arrays, which we assume are
            # the most common thing passing through here.
            return result.reshape(self.shape)
        except (AttributeError, TypeError, NotImplementedError):
            return result

    @property
    def is_symbolic(self):
        return self.symbols() != {}

    def add_or_get_node(self, value):
        if value is None:
            raise TypeError('unsupported operand for \'NoneType\'')
        if value is self:
            assert self.head is not None
            return self.head

        if isinstance(value, ExpressionGraph):
            return self.merge_and_return_subgraph_head(value)

        idx = len(self.nodes)
        if is_op(value):
            self.nodes.append(value)
            return idx
        # else - a scalar or matrix
        try:
            # already in the array
            return self.nodes.index(value)
        except ValueError:
            pass

        self.nodes.append(as_array(value))
        return idx

    def merge_and_return_subgraph_head(self, other):
        new_indices = {
            old_idx: self.add_or_get_node(node)
            for old_idx, node in enumerate(other.nodes)
        }
        for parent, children in other.edges.items():
            new_source_idx = new_indices[parent]
            if not children:
                continue
            self.edges[new_source_idx] += [
                new_indices[child] for child in children
            ]
        return new_indices[other.head]

    def push_op(self, op, *nodes):
        """Add a new operation (trunk) to the expression tree."""
        op_node = self.add_or_get_node(op)
        node_indices = [self.add_or_get_node(node) for node in nodes]
        self.edges[op_node] = node_indices
        self.head = op_node
        assert self.shape

        return self

    def __iadd__(self, other):
        return self.push_op(add, self, other)

    def __isub__(self, other):
        return self.push_op(sub, self, other)

    def __imul__(self, other):
        return self.push_op(mul, self, other)

    def __idiv__(self, other):
        return self.push_op(div, self, other)

    def __imatmul__(self, other):
        return self.push_op(matmul, self, other)

    def __hash__(self):
        edge_list = sorted(list(
            (parent, child) for parent, children in self.edges.items()
            for child in children
        ))
        edge_hash = hash(tuple(edge_list))

        def hash_nodes():
            hashes = []
            for node in self.nodes:
                hashes.append(hash(node))
            return hashes

        return hash((edge_hash, *hash_nodes()))

    def symbols(self):
        def recurse(node):
            obj = self.nodes[node]
            if not is_op(obj):
                try:
                    return obj.symbols()
                except AttributeError:
                    return set()

            child_symbols = set.union(
                    *(recurse(child)
                      for child in self.edges[node])
                )
            if obj is evaluate_signal:
                return child_symbols - {get_time_variable()}
            else:
                return child_symbols

        return recurse(self.head)

    def get_subtree_at(self, index):

        def recurse(node_idx):
            if node_idx not in self.edges:
                return self.nodes[node_idx]
            else:
                return ExpressionGraph(
                    self.nodes[node_idx],
                    *[recurse(idx) for idx in self.edges[node_idx]]
                )

        return recurse(index)

    def list_subtree(self, index):
        visited = set()
        unvisited = set(index)
        while unvisited:
            item = unvisited.pop()
            if item in visited:
                continue
            visited.add(item)
            if item in self.edges:
                unvisited |= set(self.edges[item])

        return visited

    def get_topological_sorted_indices(self):
        """Topological sort via Kahn's algorithm."""

        # Tree is organised as:
        #
        #         parent
        #         /   \
        #      child  child
        #
        # edges point from parent to child

        frontier = {self.head}

        edges = {i: l.copy() for i, l in self.edges.items() if l}
        reverse_graph = defaultdict(list)

        for in_node, out_nodes in edges.items():
            for out_node in out_nodes:
                reverse_graph[out_node].append(in_node)
        result = []
        while frontier:
            node = frontier.pop()
            result.append(node)
            if node not in edges:
                continue
            while edges[node]:
                child = edges[node].pop()
                reverse_graph[child].remove(node)
                if not reverse_graph[child]:
                    frontier.add(child)

        if any(lst != [] for lst in edges.values()):
            raise ValueError(f'Graph has cycles: {edges}')
        return result

    def is_acyclic(self):
        self.get_topological_sorted_indices()
        return True

    def __repr__(self):
        def trunk_function(node_object, *children):
            args = ','.join(children)

            string = op_to_string(node_object)

            return f'({string}: {args})'

        return recursively_apply(self, trunk_function, str)


def recursively_apply(graph: 'ExpressionGraph',
                      trunk_function,
                      leaf_function=None,
                      current_node=None):

    if leaf_function is None:
        def leaf_function(*iargs):
            return iargs

    if isinstance(graph, ConstantFunction):
        return leaf_function(graph.value)
    if isinstance(graph, GraphWrapper):
        return recursively_apply(graph.graph, trunk_function, leaf_function)
    if not isinstance(graph, ExpressionGraph):
        return leaf_function(graph)

    sorted_nodes = graph.get_topological_sorted_indices()
    trunk_indices = {i for i in sorted_nodes if i in graph.edges}
    context = {}

    while sorted_nodes:
        node = sorted_nodes.pop()
        if node in context:
            continue
        item = graph.nodes[node]
        if node in trunk_indices:
            args = [context[i] for i in graph.edges[node]]
            context[node] = trunk_function(item, *args)
        else:
            context[node] = leaf_function(item)

    return context[graph.head]


def substitute(graph: ExpressionGraph, symbols: Dict[Variable, Any]):

    def on_leaf_node(node):
        try:
            return symbols[node]
        except KeyError:
            return node

    def on_trunk_node(op, *args):
        return ExpressionGraph(op, *args)

    return recursively_apply(graph,
                             trunk_function=on_trunk_node,
                             leaf_function=on_leaf_node)


def function_from_graph(graph: ExpressionGraph, arguments: List[Variable]):

    if graph in arguments or isinstance(graph, ExpressionGraph):
        return GraphWrapper(graph, arguments)

    if graph is None:
        return None

    return ConstantFunction(graph, arguments)


class GraphWrapper(Algebraic):
    """Wraps an expression graph with the specified arguments."""

    def __init__(self, graph: ExpressionGraph, arguments: List[Variable]):
        self.arguments = tuple(arguments)

        unbound_symbols = {s for s in graph.symbols() if s not in arguments}

        if unbound_symbols:
            raise ValueError('Could not create function from graph due to'
                             f'unbound symbolic variables: {unbound_symbols}')
        self.graph = graph

    def symbols(self):
        return set(self.arguments)

    @property
    def shape(self):
        return self.graph.shape

    def call(self, args: Dict[Variable, Any]):

        symbols = self.graph.symbols()
        inner_args = {
            a: args[a] for a in self.arguments
            if a in symbols
        }
        return self.graph.call(inner_args)

    def __call__(self, *args):
        if len(args) != len(self.arguments):
            raise ValueError(
                f'Invalid arguments; expected {self.arguments}, '
                f'but recieved {args}')
        return self.call(dict(zip(self.arguments, args)))

    def __hash__(self):
        return hash((hash(self.graph), hash(tuple(self.symbols()))))

    def __repr__(self):
        return f'{self.symbols()} ->  {self.graph}'


class Inequality:
    """Inequality expression.

    Non-negative evaluation means that the inequality is satisfied.

    """
    def __init__(self, smaller, bigger):
        self.smaller = smaller
        self.bigger = bigger

    def __repr__(self):
        return f'{self.smaller} <= {self.bigger}'

    def symbols(self):
        result = set()
        for term in (self.smaller, self.bigger):
            try:
                result |= term.symbols()
            except AttributeError:
                pass

        return result

    def to_graph(self):
        return self.bigger - self.smaller

    def call(self, args):
        return self.to_graph().call(args)


class PathInequality(Inequality):
    """
        Non-negative evaluation means that the inequality is satisfied.

    """
    def to_ode(self, regulariser, alpha=1):
        """
        Implements the K-S functional
        math::
            c(g,rho) = ln(int_0^t exp[- rho*g ]dt/alpha)/rho

        Args:
            regulariser:
            alpha:      Weighting constant

        Returns:
            c, dc/dt - where c is the variable and dc/dt is an expression graph
            for the dynamics. Where c < zero as rho-> infity implies
            the constraint is violated.

        """

        c = Variable('c')
        rho = regulariser
        g = self.to_graph()

        return c, np.exp(rho * (c - g)) / (alpha * rho)


class SignalReference(Algebraic):
    """Symbolic variable representing a time varying signal.

    Args:
        port: The model port from which this signal is derived.

    """

    _signals = {}

    def __init__(self, port):
        self.port = port
        self._context = None

    def __new__(cls, port):
        source_id = id(port)
        try:
            new_signal = SignalReference._signals[source_id]()
            assert new_signal is not None
            return new_signal
        except (KeyError, AssertionError):
            pass
        new_signal = super().__new__(cls)
        SignalReference._signals[source_id] = weakref.ref(new_signal)
        return new_signal

    def __repr__(self):
        return str(self.port)

    @property
    def t(self):
        if not self._context:
            return get_time_variable()
        else:
            return self._context.t

    @property
    def shape(self):
        return len(self.port),

    def __hash__(self):
        return hash(self.port)

    def __eq__(self, other):
        try:
            return self.port is other.port
        except AttributeError:
            return False

    def __cmp__(self, other):
        try:
            return self.port is other.port
        except AttributeError:
            return False

    def __call__(self, t):
        if t is get_time_variable():
            return self
        try:
            self._context = t.context
        except AttributeError:
            pass
        return ExpressionGraph(evaluate_signal, self, t)

    def symbols(self):
        return {self, self.t}

    def call(self, args):
        function = args[self]
        if isinstance(function, ExpressionGraph):
            result = function
        else:
            result = Function(self.shape, function, [self.t])

        if self.t in args:
            return result.call(args)
        else:
            return result


@register_op(string='call')
def evaluate_signal(signal: Callable, t: Union[Variable, float]):
    """Evaluates the signal at the given time."""
    return signal(t)


def replace_signal(graph: ExpressionGraph, port, time, subs):

    def leaf_function(obj):
        return obj

    def trunk_func(obj, *args):
        # pylint: disable=comparison-with-callable
        if obj == evaluate_signal:
            signal_ref, eval_time = args
            # todo: should not be comparing by string (SYS-80)
            if str(signal_ref.port) == str(port) and eval_time == time:
                return subs
            else:
                print(f'{eval_time}, {time}')

        return ExpressionGraph(obj, *args)

    return recursively_apply(graph, trunk_func, leaf_function)


_t = Variable('time')


def get_time_variable():
    """Gets the common time variable."""
    return _t


def _is_subtree_constant(graph, node):
    obj = graph.nodes[node]
    if not is_op(obj):
        return not is_temporal(obj)
    if obj is evaluate_signal:
        return True
    return all(
        _is_subtree_constant(graph, child) for child in graph.edges[node]
    )


class Quadrature(Algebraic):
    """Variable representing a quadrature."""

    def __init__(self, integrand, context):
        self.integrand = integrand
        self._context = weakref.ref(context)
        self._index = None
        self.index = context.add_quadrature(integrand)

    def __repr__(self):
        return f'(int_0^t {str(self.integrand)} dt'

    @property
    def shape(self):
        return self.integrand.shape

    @property
    def context(self):
        return self._context()

    def __hash__(self):
        return id(self)

    def symbols(self):
        return self.integrand.symbols()

    def __call__(self, t, *args):
        return self.context.evaluate_quadrature(self.index, t, *args)


class ConstantFunction(Algebraic):
    """Wrap a constant value and treat it like a function."""

    def __init__(self, value, arguments: List[Variable]):
        if isinstance(value, np.ndarray):
            self.value = value.view(Matrix)
        elif isinstance(value, (list, tuple)):
            self.value = np.array(value).view(Matrix)
        else:
            self.value = as_array(value)

        self.arguments = arguments

    def __hash__(self):
        return hash((*self.arguments, self.value))

    @property
    def shape(self):
        if isinstance(self.value, (float, int)):
            return scalar_shape
        else:
            return self.value.shape

    def __repr__(self):
        return str(self.value)

    def symbols(self):
        return self.arguments

    def __call__(self, *args, **kwargs):
        return self.value


def is_symbolic(arg):
    if isinstance(arg, list):
        return any(is_symbolic(a) for a in arg)
    if isinstance(arg,  Algebraic):
        return len(arg.symbols()) > 0
    try:
        return arg.is_symbolic
    except AttributeError:
        return False


def is_vector_like(arg):
    if is_matrix(arg):
        return len(arg.shape) == 1 or (
            len(arg.shape) == 2 and arg.shape[1] == 1)
    return False


def is_scalar(item):
    if isinstance(item, (float, int, complex)):
        return True
    try:
        return item.shape == scalar_shape
    except AttributeError:
        pass
    return False


def is_zero(arg, shape=scalar_shape):
    try:
        r = bool(arg == 0)
        return r
    except ValueError:
        pass
    try:
        return arg.shape == shape and (arg == 0).all()
    except AttributeError:
        pass
    return False


def is_temporal(symbol):

    if isinstance(symbol, PathInequality):
        return True
    if isinstance(symbol, ExpressionGraph):
        return not _is_subtree_constant(symbol, symbol.head)
    if isinstance(symbol, SignalReference):
        return True
    if symbol is get_time_variable():
        return True
    if is_op(symbol):
        return False
    return False


def is_matrix(obj):
    return isinstance(obj, (np.ndarray, Matrix, SparseMatrix))

