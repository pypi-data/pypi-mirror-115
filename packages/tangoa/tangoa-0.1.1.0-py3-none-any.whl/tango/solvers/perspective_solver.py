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

from tangoa.helper import to_binary
from tangoa.objectives import psi_bar
from tangoa.runtime import Timer
from tangoa.solvers.solver_skeleton import SolverSkeleton


class PerspectiveSolver(SolverSkeleton):
    def __init__(self, Q, b, c, d, warmstart=None, **kwargs):
        super().__init__(Q, b, c, d, **kwargs)
        self.complete_runtime = 0
        self.timer = Timer()
        self.timer.start()
        self.warmstart = warmstart

        self.H = self.Q - self.D

        self.init_gurobi()
        self.timer.stop()

    def init_gurobi(self):
        self.env = gp.Env(empty=True)
        self.env.setParam("OutputFlag", not self.mute)
        self.env.start()
        self.model = gp.Model("Tango_Perspective", env=self.env)

        self._build_variables()
        self._build_model()
        self._build_objective()

    def _add_x(self):
        self.var_x = self.model.addVars(range(self.n), name="x", lb=-float("inf"))
        for i in range(self.n):
            self.x_inds[self.var_x[i].index] = i

    def _add_z(self):
        self.var_z = self.model.addVars(range(self.n), vtype=GRB.BINARY, name="z")
        for i in range(self.n):
            self.z_inds[self.var_z[i].index] = i

    def _build_variables(self):
        self._add_x()
        self._add_z()
        self.var_eta = self.model.addVar(name="eta", lb=-float("inf"))
        self.var_tau = self.model.addVars(range(self.n), name="tau")

    def _build_model(self):
        for i in range(self.n):
            self.model.addConstr(0.5 * self.d[i] * (self.var_x[i] ** 2) <= self.var_z[i] * self.var_tau[i])
        expr = 0
        nzs = np.nonzero(self.H)
        for i, j in zip(nzs[0], nzs[1]):
            expr += 0.5 * self.H[i, j] * self.var_x[i] * self.var_x[j]
        for i in range(self.n):
            expr += self.var_tau[i]
            expr -= self.b[i] * self.var_x[i]
            expr += self.c[i] * self.var_z[i]
        self.model.addConstr(self.var_eta / self.objective_scalar >= expr)
        self.model.addConstr(gp.quicksum([self.var_z[i] for i in range(self.n)]) >= 1)

    def _build_objective(self):
        self.model.setObjective(self.var_eta, GRB.MINIMIZE)

    def add_z_constr(self, constr):
        self.timer.start()
        self.model.addConstr(constr)
        self.timer.stop()

    def add_x_eq_constr(self, lin_expr, rhs):
        self.timer.start()
        super().add_x_eq_constr(lin_expr, rhs)
        self.model.addConstr(lin_expr == rhs)
        self.timer.stop()

    def add_x_ineq_constr(self, lin_expr, rhs):
        self.timer.start()
        super().add_x_ineq_constr(lin_expr, rhs)
        self.model.addConstr(lin_expr >= rhs)
        self.timer.stop()

    def _hand_warmstart_to_gurobi(self):
        if self.warmstart is not None:
            for i in range(self.n):
                self.var_z[i].start = to_binary(self.warmstart[i])
            self.var_eta.start = psi_bar(to_binary(self.warmstart), self)

    def solve(self):
        self.timer.start()
        self._hand_over_data()
        if self.time_limit is not None:
            self.model.setParam(GRB.Param.TimeLimit, self.time_limit)

        self.model.Params.Threads = 1
        self.model.setParam("OutputFlag", not self.mute)

        self.model.optimize()
        ret = self._eval_after_solve(sanity_tol=1e-2, compute_x=False)
        self.timer.stop()
        self.complete_runtime = self.timer.elapsed_time
        self.timer.reset()
        return ret
