#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import numpy as np

from tangoa.model_parameters import ObjectiveParameters
from tangoa.solvers.subsolvers.GurobiQPSolver import GurobiQPSolver


def perspective_objective_value(x: np.ndarray, z: np.ndarray, *args):
    """
        Computes the objective value of the perspective objective, given a feasible x and z.

    :param x: Feasible point x.
    :param z: Feasible indicator variables z. The square root of them is taken in the procedure. Only values in the interval [0, 1] are valid.
    :param args: Arguments for ObjectiveParameters.
    :return: Objective value.
    """
    params = ObjectiveParameters(*args)
    sz = np.sqrt(z)
    szx = sz * x
    ret = 0.5 * szx.transpose().dot(params.H.dot(szx))
    ret += 0.5 * x.transpose().dot(params.D.dot(x))
    ret -= params.b.transpose().dot(szx)
    ret += params.c.transpose().dot(z)
    return ret


def phi(x: np.ndarray, z: np.ndarray, *args):
    params = ObjectiveParameters(*args)
    zx = z * x
    ret = 0.5 * zx.transpose().dot(params.H.dot(zx))
    ret += 0.5 * x.transpose().dot(params.D.dot(x))
    ret -= params.b.transpose().dot(zx)
    ret += params.c.transpose().dot(z)
    return ret


def psi_bar(z, *args: np.array, objective_scalar=1.0, qpsolver_class=None, qpsolver=None, **kwargs):
    if qpsolver is None:
        if qpsolver_class is not None:
            solver = qpsolver_class(*args, objective_scalar=objective_scalar, **kwargs)
        else:
            solver = GurobiQPSolver(*args, objective_scalar=objective_scalar, **kwargs)
    else:
        solver = qpsolver
    solver.solve(z)
    return perspective_objective_value(solver.x, z, *solver.get_args())
