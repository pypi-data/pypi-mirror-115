#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import gurobipy as gp
from gurobipy import GRB
import numpy as np
import scipy as sp
from scipy.sparse import issparse
from scipy.sparse.linalg import spsolve, lsqr
from numpy.linalg import solve

from tangoa.helper import diag, to_binary, to_array
from tangoa.model_parameters import ModelParameters


class GurobiQPSolver(ModelParameters):
    def __init__(self, *args, A=None, w=None, G=None, u=None, **kwargs):
        super().__init__(*args, A=A, w=w, G=G, u=u, **kwargs)
        self.x = None
        self.mu = None
        self.lam = None
        self.feasible = False

        self.env = None
        self.model = None

        self.var_x = None
        self.var_y = None

        self.ineq_cons = None
        self.coupling_cons = None

        self._init_gurobi()

    def _init_gurobi(self):
        self.env = gp.Env(empty=True)
        self.env.setParam("OutputFlag", 0)
        self.env.start()
        self.model = gp.Model("Subsolver", env=self.env)
        self.model.setParam("OutputFlag", 0)

        self._build_variables()
        self._build_model()
        self._build_objective()

    def _build_variables(self):
        self.var_x = self.model.addMVar(self.n, lb=-float("inf"))
        self.var_y = self.model.addMVar(self.n, lb=-float("inf"))

    def _build_model(self):
        self.model.addConstr(self.A @ self.var_y == self.w)
        self.ineq_cons = self.model.addConstr(self.G @ self.var_y >= self.u)

    def _build_objective(self):
        expr1 = self.var_y @ self.H @ self.var_y
        expr2 = self.var_x @ self.D @ self.var_x
        expr3 = self.b @ self.var_y
        self.model.setObjective(0.5 * expr1 + 0.5 * expr2 - expr3)

    def solve(self, z):
        if self.coupling_cons is not None:
            self.model.remove(self.coupling_cons)

        sz_diag = diag(np.sqrt(np.clip(z, 0, 1)))
        self.coupling_cons = self.model.addConstr(self.var_y == sz_diag @ self.var_x)

        self.model.optimize()
        status = self.model.getAttr("Status")
        if status == GRB.INFEASIBLE or status == GRB.INF_OR_UNBD:
            self.feasible = False
            return False
        self.x = self.var_x.x
        self._compute_dual_values(sz_diag)
        self.feasible = True
        return True

    def _compute_dual_values(self, sz_diag):
        self.lam = self.ineq_cons.getAttr("Pi")
        lhs = sz_diag @ self.A.transpose()
        rhs = to_array(sz_diag @ self.H @ sz_diag @ self.x + self.D @ self.x - sz_diag @ self.G.transpose() @ self.lam - sz_diag @ self.b)
        if issparse(lhs):
            self.mu = lsqr(lhs, rhs)[0]
        else:
            self.mu = solve(lhs, rhs)

    def __del__(self):
        if self.model is not None:
            del self.model
        if self.env is not None:
            del self.env
