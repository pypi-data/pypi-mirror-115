#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import numpy as np
import gurobipy as gp
from gurobipy import GRB

from tangoa.solvers.basic_solver_skeleton import BasicSolverSkeleton


class PerspectiveRelaxation(BasicSolverSkeleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.H = self.Q - self.D

        self.var_tau = None

        self.init_gurobi()

    def get_z(self):
        return self.var_z

    def get_x(self):
        return self.var_x

    def _build_variables(self):
        self.var_x = self.model.addVars(range(self.n), name="x", lb=-float("inf"), ub=float("inf"))
        self.var_z = self.model.addVars(range(self.n), name="z", ub=1.0)
        self.var_tau = self.model.addVars(range(self.n), name="tau")

    def _build_model(self):
        for i in range(self.n):
            self.model.addConstr(0.5 * self.d[i] * (self.var_x[i] ** 2) <= self.var_z[i] * self.var_tau[i])
        self.model.addConstr(gp.quicksum([self.var_z[i] for i in range(self.n)]) >= 1)

    def _build_objective(self):
        nzs = np.nonzero(self.H)
        expr = 0
        for i, j in zip(nzs[0], nzs[1]):
            expr += 0.5 * self.H[i, j] * self.var_x[i] * self.var_x[j]
        for i in range(self.n):
            expr += self.var_tau[i]
            expr -= self.b[i] * self.var_x[i]
            expr += self.c[i] * self.var_z[i]
        self.model.setObjective(self.objective_scalar * expr, GRB.MINIMIZE)

    def add_z_constr(self, constr):
        self.model.addConstr(constr)

    def init_gurobi(self):
        self.env = gp.Env(empty=True)
        self.env.setParam("OutputFlag", not self.mute)
        self.env.start()
        self.model = gp.Model("Tango_perspective_relaxation", env=self.env)

        self._build_variables()
        self._build_model()
        self._build_objective()

    def solve(self):
        self.model.Params.Threads = 1
        self.model.setParam("OutputFlag", not self.mute)
        self.model.optimize()

        return self._eval_after_solve()
