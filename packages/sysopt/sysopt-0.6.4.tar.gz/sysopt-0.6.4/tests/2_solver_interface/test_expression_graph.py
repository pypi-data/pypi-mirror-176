from sysopt.symbolic import (
    Variable, is_symbolic,
    is_temporal, ExpressionGraph, PathInequality
)

from sysopt.symbolic.core import get_time_variable, unary

from sysopt.blocks import Gain, Oscillator
from sysopt.modelling.block import Composite

import numpy as np


def test_variables_api():

    d = Variable()
    d2 = Variable()
    assert is_symbolic(d)
    expressions = [d + 2, d - 2, -d, 2-d, 2+d, d/2, 2 / d, 2 * d, d*2, d + d2]

    for expression in expressions:
        assert is_symbolic(expression)
        assert d in expression.symbols()

    for op in unary:
        result = op(d)
        assert is_symbolic(result)
        assert d in expression.symbols()


class TestSignalApi:
    def test_create_and_evaluate(self):
        source = Oscillator()

        t = get_time_variable()
        sig = source.outputs(t)
        assert sig is not None
        assert sig.port is source.outputs
        expr = sig(0)

        assert expr is not None
        assert expr is not sig

        assert isinstance(expr, ExpressionGraph)

    def test_identity(self):
        gain = Gain(2)
        t = get_time_variable()
        sig_0 = gain.outputs[0](t)
        sig_1 = gain.outputs[1](t)

        assert sig_0.symbols() == sig_1.symbols()


def test_is_temporal():
    var = Variable()
    source = Oscillator()
    t = get_time_variable()
    sig = source.outputs(t)

    assert not is_temporal(var)
    assert is_temporal(sig)
    assert is_temporal(var + sig)

    assert not is_temporal(sig(0))
    assert not is_temporal(sig(1))


def test_evaluate_graph():

    def y(tau):
        return np.exp(tau)

    var = Variable()
    source = Oscillator()
    t = get_time_variable()
    sig = source.outputs(t)
    param = Variable()

    expression = 1 + var * sig(1) + param
    values = {
        var: 2,
        sig: y,
        param: 3
    }
    expected_result = 1 + 2 * np.exp(1) + 3

    assert expression.symbols() == {var, sig, param}

    result = expression.call(values)
    assert result == expected_result


def test_inequality_to_function():
    var = Variable()
    var_inequality = var <= 1

    assert var_inequality.call({var: 2}) < 0
    assert var_inequality.call({var: 1}) == 0
    assert var_inequality.call({var: 0}) > 0

    f = var_inequality.to_graph()
    assert f(2) < 0
    assert f(1) == 0
    assert f(0) > 0


def test_supremum_to_function():
    t = get_time_variable()
    source = Oscillator()
    sig = source.outputs(t)
    param = Variable()

    def y(t_):
        return np.exp(-t_)

    supremum = sig(t) < param
    assert isinstance(supremum, PathInequality)

    expr = supremum.call({param: 2, sig: y})

    assert expr.symbols() == {t}
    result = expr.call({t: 0})
    assert result > 0


def test_graph_merging():

    a = Variable('a')
    b = Variable('b')

    graph_1 = 1 + a ** 2
    graph_2 = 1 - b ** 2
    graph_3 = graph_1 - graph_2 + 2 * a * b
    dummy_var = graph_3 + 2
    values = {a: 3, b: 5}
    result = graph_3.call(values)
    assert result == 8 ** 2
    assert dummy_var.call(values) == 8 ** 2 + 2

# Optimisation problem setup for a model m
# 1. Assemble flattened system s from m
# 2. Add
# 3. Add quadrature for loss function
# 4. Add constraint dynamics



