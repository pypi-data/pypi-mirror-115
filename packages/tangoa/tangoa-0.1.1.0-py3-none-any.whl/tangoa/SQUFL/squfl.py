#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import gurobipy as gp
import numpy as np

from tangoa.helper import diag
from tangoa.solvers.oa import OASolver


class SeparableQuadraticUFL:
    def __init__(self, Q, c, solver=OASolver, time_limit=None, percent_extraction=1.0, **kwargs):
        self.Q = Q
        self.c = c
        self.n_facilities = self.Q.shape[0]
        self.n_customers = self.Q.shape[1]
        self.n = self.n_customers * self.n_facilities
        d = np.zeros(self.n)
        c_extended = np.zeros(self.n)
        q = np.zeros(self.n)
        for i in range(self.n_facilities):
            for j in range(self.n_customers):
                d[self.n_customers * i + j] = percent_extraction * self.Q[i, j]
                q[self.n_customers * i + j] = self.Q[i, j]
                c_extended[self.n_customers * i + j] = self.c[i] / self.n_customers
        self.solver = solver(2 * diag(q), np.zeros(self.n), c_extended,
                             2 * d, time_limit=time_limit, **kwargs)
        var_z = self.solver.get_z()
        var_x = self.solver.get_x()
        for i in range(self.n_facilities):
            for j in range(self.n_customers - 1):
                self.solver.add_z_constr(var_z[self.n_customers * i + j] == var_z[self.n_customers * i + j + 1])
        for j in range(self.n_customers):
            self.solver.add_x_eq_constr(
                gp.quicksum([var_x[self.n_customers * i + j] for i in range(self.n_facilities)]),
                1)
        for i in range(self.n):
            self.solver.add_x_ineq_constr(1.0 * var_x[i], 0)

    def solve(self):
        return self.solver.solve()
