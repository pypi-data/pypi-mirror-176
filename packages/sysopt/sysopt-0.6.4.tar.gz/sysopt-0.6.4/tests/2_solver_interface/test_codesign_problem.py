import sympy as sp
from sysopt.modelling.types import *
from sysopt.modelling.block import Block
from sysopt.problems.solver import SolverContext, get_time_variable
from sysopt.modelling.block import Composite
from sysopt.modelling.builders import FullStateOutput
from sysopt.blocks import ConstantSignal
from sysopt.symbolic import Variable, PiecewiseConstantSignal


class LinearScalarEquation(Block):
    r"""Linear ODE of the form

    math::
        \dot{x} = -ax
        x(0)  = x_0

    """

    def __init__(self):
        metadata = Metadata(
            inputs=[],
            outputs=['y'],
            states=['x'],
            constraints=[],
            parameters=['a', 'x0']
        )
        super().__init__(metadata, 'dx')

    def initial_state(self, parameters: Parameters) -> Numeric:
        _, x0 = parameters
        return x0

    def compute_dynamics(self,
                         t: Time,
                         states: States,
                         algebraics: Algebraics,
                         inputs: Inputs,
                         parameters: Parameters):
        x, = states
        a, _ = parameters
        return -x*a

    def compute_outputs(self,
                        t: Time,
                        states: States,
                        algebraics: Algebraics,
                        inputs: Inputs,
                        parameters: Parameters) -> Numeric:
        x, = states
        return x

    def explicit_solution(self, t, parameters):
        a, x0 = parameters
        return np.exp(-a * t) * x0

    def dxdp(self, t, parameters):
        a, x0 = parameters
        return [
            -t * a * np.exp(-a*t) * x0,
            np.exp(-a * t)
        ]

    def pushforward(self, t,  p, dp):
        x = self.explicit_solution(t, p)
        a, x0 = p
        return [
            -t * a * x * dp[0] + x * dp[1] / x0
        ]


class Problem1:
    @staticmethod
    def symbolic_cost():
        t, a, x0 = sp.symbols('t ,a, x0')
        x = x0 * sp.exp(-a * t)
        j = Problem1.running_cost(x)
        cost = sp.integrate(j, (t, 0, t)) - x
        return cost, a, x0, t

    @staticmethod
    def running_cost(y):
        return - y ** 2

    @staticmethod
    def cost(t, params):
        a, x0 = params
        cost, *symbols = Problem1.symbolic_cost()
        subs = dict(zip(symbols, [a,x0, t]))
        result = float(cost.evalf(subs=subs))
        return result
        # return x0**2 *(np.exp(-2*a * t) - 1) / (2 * a)

    @staticmethod
    def tangent_space(params, t):
        cost, sa, sx0, st = Problem1.symbolic_cost()
        a, x0 = params
        subs = {sa: a, sx0: x0, st: t}
        dfda = sp.diff(cost, sa).evalf(subs=subs)
        dfdx0 = sp.diff(cost, sx0).evalf(subs=subs)
        return np.array([[dfda], [dfdx0]])


def test_codesign_problem_1():
    block = LinearScalarEquation()
    parameters = {
        block.parameters[0]: Variable('a', 1),
        block.parameters[1]: Variable('x0', 1)
    }

    with SolverContext(model=block,
                       parameters=parameters,
                       t_final=1) as solver:
        params = solver.parameters

        assert len(params) == 2

        constraints = [
            0.5 < params[0] < 1,
            0.5 < params[1] < 1
        ]
        t = solver.t
        y = block.outputs(t)

        running_cost = -y ** 2
        p0 = [0.75, 0.75]

        cost = solver.integral(running_cost) - y(1)
        problem = solver.problem(params, cost, constraints)

        result = float(problem(p0)[0])

        assert abs(result - Problem1.cost(1, p0)) < 1e-4

        jac = problem.jacobian(p0)
        assert jac.shape == (2, 1)

        grad_known = Problem1.tangent_space(p0, t=1)
        assert (jac - grad_known < 1e-4).all()


def test_codesign_problem_with_path_variable(linear_model):

    u = PiecewiseConstantSignal('u', frequency=10)
    t_final = Variable('t_f')

    parameters = {linear_model.parameters[0]: u}

    with SolverContext(linear_model,
                       parameters=parameters,
                       t_final=t_final) as context:

        y = linear_model.outputs(t_final)
        constraint = [
            y[0:2].T @ y[0:2] < 1e-9,
            u <= 1,
            u >= -1
        ]
        problem = context.problem(
            [t_final, u],
            cost=t_final,
            subject_to=constraint
        )
        spec = problem._get_minimisation_specification()
        assert u in spec.parameters
        assert t_final in spec.parameters
        p, = spec.parameter_map.symbols()
        t = get_time_variable()
        expected_symbols = {
            p, get_time_variable(),
            linear_model.outputs(t)
        }
        q, = spec.value.symbols() - expected_symbols
        expected_symbols.add(q)
        assert spec.parameters[u] == [-1, 1]

        assert len(spec.point_constraints) == 1
        constraint, = spec.point_constraints
        assert constraint.symbols() == expected_symbols
        y_f_test = np.array([1, 1, 0])
        result = constraint(0, y_f_test, None, np.array([1, 1]))
        assert result < -1.9, "Result should be near -2, with satisfaction >=0"
