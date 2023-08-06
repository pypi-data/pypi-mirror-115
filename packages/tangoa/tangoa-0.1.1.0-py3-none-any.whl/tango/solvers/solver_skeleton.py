#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import abc

import numpy as np
from gurobipy import GRB
from scipy.sparse import csc_matrix

from tangoa.helper import to_binary
from tangoa.model_parameters import ModelParameters
from tangoa.objectives import psi_bar, perspective_objective_value
from tangoa.solvers.basic_solver_skeleton import BasicSolverSkeleton
from tangoa.solvers.subsolvers.GurobiQPSolver import GurobiQPSolver


class SolverSkeleton(BasicSolverSkeleton, abc.ABC):
    def __init__(self, *args, **kwargs):
        self.a_list = []
        self.w_list = []
        self.g_list = []
        self.u_list = []

        self.A = None
        self.w = None
        self.G = None
        self.u = None

        self.eq_changed = True
        self.ineq_changed = True
        self.var_eta = None

        self.x_inds = dict()
        self.z_inds = dict()

        self.was_hand_over = False

        if "qpsolver_class" in kwargs.keys():
            self.qpsolver_class = kwargs["qpsolver_class"]
        else:
            self.qpsolver_class = None

        self.qpsolver = None
        self.qpsolver_initialized = False

        super().__init__(*args, **kwargs)

    @abc.abstractmethod
    def _hand_warmstart_to_gurobi(self):
        pass

    def add_x_eq_constr(self, lin_expr, rhs):
        self._add_x_constr(lin_expr, rhs, self.a_list, self.w_list, ineq=False)

    def add_x_ineq_constr(self, lin_expr, rhs):
        self._add_x_constr(lin_expr, rhs, self.g_list, self.u_list)

    def _add_x_constr(self, lin_expr, rhs, lhs_list, rhs_list, ineq=True):
        self.model.update()
        for i in range(lin_expr.size()):
            var = lin_expr.getVar(i)
            if var.getAttr("VType") == GRB.BINARY:
                raise Exception("Linear expression contains z variables.")
            else:
                if ineq:
                    lhs_list.append((self.l, self.x_inds[var.index], lin_expr.getCoeff(i)))
                else:
                    lhs_list.append((self.m, self.x_inds[var.index], lin_expr.getCoeff(i)))
        if ineq:
            rhs_list.append((self.l, -lin_expr.getConstant() + rhs))
        else:
            rhs_list.append((self.m, -lin_expr.getConstant() + rhs))
        if ineq:
            self.l += 1
        else:
            self.m += 1
        if ineq:
            self.ineq_changed = True
        else:
            self.eq_changed = True

    def get_A(self):
        self._build_constraint_matrices()
        return self.A

    def get_w(self):
        self._build_constraint_matrices()
        return self.w

    def get_G(self):
        self._build_constraint_matrices()
        return self.G

    def get_u(self):
        self._build_constraint_matrices()
        return self.u

    def get_model_parameters(self):
        self._build_constraint_matrices()
        self._hand_over_data()
        return self.model._params

    def _build_constraint_matrices(self):
        def build_lhs_and_rhs_from_list(lhs, rhs, lhs_list, rhs_list, n, was_changed):
            if was_changed:
                l = len(rhs_list)
                if l > 0:
                    lhs_data = list()
                    lhs_rows = list()
                    lhs_cols = list()
                    rhs = np.zeros(l)
                    for i, j, entry in lhs_list:
                        # lhs[i, j] = entry
                        lhs_data.append(entry)
                        lhs_rows.append(i)
                        lhs_cols.append(j)
                    for i, entry in rhs_list:
                        rhs[i] = entry
                    lhs = csc_matrix((lhs_data, (lhs_rows, lhs_cols)))
                else:
                    lhs = None
                    rhs = None
                was_changed = False
            return lhs, rhs, was_changed

        self.A, self.w, self.eq_changed = build_lhs_and_rhs_from_list(self.A, self.w, self.a_list, self.w_list, self.n,
                                                                      self.eq_changed)
        self.G, self.u, self.ineq_changed = build_lhs_and_rhs_from_list(self.G, self.u, self.g_list, self.u_list,
                                                                        self.n, self.ineq_changed)

    def _hand_over_data(self):
        if not self.was_hand_over:
            params = ModelParameters(self.Q, self.b, self.c, self.d, A=self.get_A(), w=self.get_w(), G=self.get_G(),
                                     u=self.get_u(), objective_scalar=self.objective_scalar)
            self.model._params = params
            self.model._var_eta = self.var_eta
            self.model._var_z = self.var_z
            self.model._objective_scalar = self.objective_scalar
            self.model._cut_offs = []
            self.model._user_cuts_count = 0
            self.model._mute = self.mute
            self.model.update()
            self.was_hand_over = True

    def _init_qpsolver(self):
        assert self.was_hand_over, "_hand_over_data was not called."
        if not self.qpsolver_initialized:
            if self.qpsolver_class is not None:
                self.qpsolver = self.qpsolver_class(self.model._params)
            else:
                self.qpsolver = GurobiQPSolver(self.model._params)
            self.qpsolver_initialized = True

    def _eval_after_solve(self, compute_x=False, sanity_tol=1e-5, binary_z=True):
        if not compute_x:
            x = np.zeros(self.n)
        z = np.zeros(self.n)
        for i in range(self.n):
            if not compute_x:
                x[i] = self.var_x[i].x
            z[i] = self.var_z[i].x
        if binary_z:
            z = to_binary(z)
        else:
            z = np.clip(z, 0, 1)
        if compute_x:
            self._init_qpsolver()
            self.qpsolver.solve(z)
            x = self.qpsolver.x
        # objval = self.model.getAttr(GRB.Attr.ObjVal)
        objective_value = self.model.objVal
        check_objective_value = perspective_objective_value(x, z, self)
        # ps = psi_bar(z, self.Q, self.b, self.c, self.d, A=self.get_A(), w=self.get_w(), G=self.get_G(), u=self.get_u())
        if abs(check_objective_value - objective_value / self.objective_scalar) > sanity_tol:
            raise RuntimeError(
                "Returned objective value not equal to computed objective value. Actual obj. value is " + str(
                    check_objective_value) + " vs. reported obj. value " + str(objective_value / self.objective_scalar))
        return z, x, objective_value / self.objective_scalar
