#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from collections import Iterable

import gurobipy as gp
from gurobipy import GRB
import numpy as np
from tangoa.solvers.callbacks.callback import get_callback

from tangoa.solvers.oa import OASolver


class PortfolioOptimization:
    def __init__(self, sigma, mean_return, minimum_return, k, solver=OASolver, percent_extraction=1.0, time_limit=None,
                 d=None, x_lowerbounds=0, x_upperbounds=1, mute=False, **kwargs):
        self.sigma = sigma
        self.r = mean_return
        self.k = k
        self.n = len(self.r)
        self.method = solver
        self.mute = mute
        if not isinstance(x_lowerbounds, Iterable):
            x_lowerbounds = np.array([x_lowerbounds] * self.n)
        if not isinstance(x_upperbounds, Iterable):
            x_upperbounds = np.array([x_upperbounds] * self.n)
        if d is None:
            min_ev = min(np.linalg.eigvals(self.sigma))
            if min_ev <= 1e-8:
                raise RuntimeError("Sigma not positive definite.")
            d = percent_extraction * min_ev * np.ones(self.n)
        self.solver = solver(self.sigma, np.zeros(self.n), np.zeros(self.n),
                             d, time_limit=time_limit, mute=self.mute, **kwargs)
        var_z = self.solver.get_z()
        var_x = self.solver.get_x()
        self.solver.add_z_constr(gp.quicksum([var_z[i] for i in range(self.n)]) == k)
        self.solver.add_x_ineq_constr(gp.quicksum([mean_return[i] * var_x[i] for i in range(self.n)]), minimum_return)
        self.solver.add_x_eq_constr(gp.quicksum([var_x[i] for i in range(self.n)]), 1)
        for i in range(self.n):
            self.solver.add_x_ineq_constr(1.0 * var_x[i], x_lowerbounds[i])
            self.solver.add_x_ineq_constr(-1.0 * var_x[i], -x_upperbounds[i])

    def solve(self):
        return self.solver.solve()
