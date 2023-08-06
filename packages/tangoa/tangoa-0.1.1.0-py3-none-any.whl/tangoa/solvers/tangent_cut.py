#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import gurobipy as gp
import numpy as np
from threadpoolctl import threadpool_limits

from tangoa.helper import as_scalar, nonzeros
from tangoa.model_parameters import ModelParameters
from tangoa.objectives import perspective_objective_value
from tangoa.solvers.subsolvers.GurobiQPSolver import GurobiQPSolver


class TangentCut(ModelParameters):
    def __init__(self, *args, A=None, w=None, G=None, u=None, **kwargs):
        super().__init__(*args, A=A, w=w, G=G, u=u, **kwargs)

        if "qpsolver_class" in kwargs.keys() and kwargs["qpsolver_class"] is not None:
            self.qpsolver = kwargs["qpsolver_class"](self)
        else:
            self.qpsolver = GurobiQPSolver(self)
        self.support = None
        self.coefs = None
        self.last_z = None
        self.last_d = None

        self.feasibility_cut = False

    def just_run_qp_solver(self, z: np.array, d: np.array = None):
        # TODO: use d for solver
        self.qpsolver.solve(z)

    def compute(self, z: np.array, d: np.array = None, do_not_call_solver: bool = False):
        self.last_z = z
        self.last_d = d
        if d is None:
            d = self.d
        # TODO: use d for solver
        if not do_not_call_solver:
            self.qpsolver.solve(z)

        if self.qpsolver.feasible:
            self.feasibility_cut = False
            self.support = perspective_objective_value(self.qpsolver.x, z, *self.get_args())
            self.coefs = self._compute_coefs(z)
        else:
            self.feasibility_cut = True
            self.coefs = np.zeros(self.n)
            nzs = nonzeros(z)
            for i in nzs:
                self.coefs[i] = 1
            self.support = len(nzs) - 1

    def delta(self, i, sqrt_z):
        s = (1 / sqrt_z[i]) * ((self.qpsolver.x[i]) ** 2)
        return s

    def gamma(self, i, sqrt_z):
        zx = sqrt_z * self.qpsolver.x
        v = as_scalar(self.b[i] - self.Q[i, :].dot(zx))
        if self.equality_cons:
            v += as_scalar(self.A[:, i].transpose().dot(self.qpsolver.mu))
        if self.inequality_cons:
            v += as_scalar(self.G[:, i].transpose().dot(self.qpsolver.lam))
        s = (v ** 2)
        return s

    def get_cut(self, var_eta, var_z):
        if self.feasibility_cut:
            return self.support >= gp.quicksum([self.coefs[i] * var_z[i] for i in range(self.n)])
        else:
            expr = self.support
            for i in range(self.n):
                expr += self.coefs[i] * (var_z[i] - self.last_z[i])
                expr += self.c[i] * (var_z[i] - self.last_z[i])
            return var_eta >= expr * self.objective_scalar

    def _compute_coefs(self, z):
        with threadpool_limits(limits=1):
            zx = np.sqrt(np.clip(z, 0, 1)) * self.qpsolver.x
            v = self.b - self.H.dot(zx) + self.A.transpose().dot(self.qpsolver.mu) + self.G.transpose().dot(
                self.qpsolver.lam)
            return - 0.5 * (v * v) / self.d
