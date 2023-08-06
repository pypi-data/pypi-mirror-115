#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import timeit

import gurobipy as gp
import numpy as np
from gurobipy import GRB

from tangoa.helper import to_binary, is_binary
from tangoa.runtime import Timer
from tangoa.solvers.callbacks.callback import get_callback
from tangoa.solvers.callbacks.output import *
from tangoa.solvers.callbacks.lazy_cuts import *
from tangoa.solvers.callbacks.incumbents import *
from tangoa.solvers.oa_solver_skeleton import OASolverSkeleton
from tangoa.solvers.relaxation.perspective_relaxation import PerspectiveRelaxation


class OASolver(OASolverSkeleton):
    def __init__(self, *args, lb=PerspectiveRelaxation, warmstart=None,
                 callbacks=(print_number_of_added_lazy_constraints,
                            print_average_cut_off,
                            print_number_of_fractional_cuts_added,
                            submit_solutions_from_lazy_callback,
                            add_lazy_constraint_if_equal_best_objective),
                 **kwargs):
        self.complete_runtime = 0
        self.timer = Timer()
        self.timer.start()
        super().__init__(*args, **kwargs)
        self.callbacks = callbacks

        self.relaxation = lb(*args, **kwargs)
        self.warmstart = warmstart
        self.init_gurobi()
        self.timer.stop()

    def init_gurobi(self):
        self.env = gp.Env(empty=True)
        self.env.setParam("OutputFlag", not self.mute)
        self.env.start()
        self.model = gp.Model("Tango_OA", env=self.env)

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

    def _hand_warmstart_to_gurobi(self):
        if self.warmstart is not None:
            for i in range(self.n):
                self.var_z[i].start = abs(np.around(self.warmstart[i]))
            self.model._tangent_cut.compute(self.warmstart, self.d)
            self.var_eta.start = self.objective_scalar * self.model._tangent_cut.support
            self.model.addConstr(
                self.model._tangent_cut.get_cut(self.var_eta, self.var_z))

    def _build_variables(self):
        self._add_x()
        self._add_z()
        self.var_eta = self.model.addVar(name="eta", lb=-float("inf"))

    def _build_model(self):
        self.model.addConstr(gp.quicksum([self.var_z[i] for i in range(self.n)]) >= 1)

    def _build_objective(self):
        self.model.setObjective(self.var_eta)

    def add_z_constr(self, constr):
        self.timer.start()
        added_constr = self.model.addConstr(constr)
        self.model.update()

        expr = self.model.getRow(added_constr)
        rel_expr = 0
        rel_z = self.relaxation.get_z()
        for i in range(expr.size()):
            j = self.z_inds[expr.getVar(i).index]
            rel_expr += expr.getCoeff(i) * rel_z[j]
        if added_constr.sense == "=":
            self.relaxation.add_z_constr(rel_expr == added_constr.rhs)
        if added_constr.sense == ">":
            self.relaxation.add_z_constr(rel_expr >= added_constr.rhs)
        if added_constr.sense == "<":
            self.relaxation.add_z_constr(rel_expr <= added_constr.rhs)
        self.timer.stop()
        return added_constr

    def add_x_eq_constr(self, lin_expr, rhs):
        self.timer.start()
        super().add_x_eq_constr(lin_expr, rhs)

        rel_expr = 0
        rel_x = self.relaxation.get_x()
        for i in range(lin_expr.size()):
            j = self.x_inds[lin_expr.getVar(i).index]
            rel_expr += lin_expr.getCoeff(i) * rel_x[j]
        self.relaxation.add_x_eq_constr(rel_expr, rhs)
        self.timer.stop()

    def add_x_ineq_constr(self, lin_expr, rhs):
        self.timer.start()
        super().add_x_ineq_constr(lin_expr, rhs)

        rel_expr = 0
        rel_x = self.relaxation.get_x()
        for i in range(lin_expr.size()):
            j = self.x_inds[lin_expr.getVar(i).index]
            rel_expr += lin_expr.getCoeff(i) * rel_x[j]
        self.relaxation.add_x_ineq_constr(rel_expr, rhs)
        self.timer.stop()

    def prepare_gurobi_for_solving(self):
        self._hand_over_data()
        self.model.remove(self.var_x)
        self.model.setParam("MIPFocus", 1)
        self.model.Params.Threads = 1
        self.model.setParam("OutputFlag", not self.mute)

        if self.time_limit is not None:
            self.model.setParam(GRB.Param.TimeLimit, self.time_limit)

        self.model.Params.lazyConstraints = 1

    def solve(self):
        self.timer.start()
        self.prepare_gurobi_for_solving()

        self.run_relaxation()

        self._hand_warmstart_to_gurobi()

        self.model.optimize(get_callback(*self.callbacks))

        self._add_x()

        ret = self._eval_after_solve(compute_x=True)
        self.timer.stop()
        self.complete_runtime = self.timer.elapsed_time
        self.timer.reset()
        return ret

    def run_relaxation(self):
        rel_z, _, rel_val = self.relaxation.solve()
        # self.var_eta.lb = rel_val
        if is_binary(rel_z):
            print("Relaxation optimal!")
        self.model._tangent_cut.compute(np.clip(rel_z, 0, 1))
        self.model.addConstr(
            self.model._tangent_cut.get_cut(self.var_eta, self.var_z),
            name="Best relaxation cut")
