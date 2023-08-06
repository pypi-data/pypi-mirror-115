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

from tangoa.model_parameters import ObjectiveParameters


class BasicSolverSkeleton(ObjectiveParameters, abc.ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.m = 0
        self.l = 0

        self.var_x = None
        self.var_z = None
        self.model = None
        self.env = None

        if "time_limit" in kwargs.keys():
            self.time_limit = kwargs["time_limit"]
        else:
            self.time_limit = None

        if "mute" in kwargs.keys():
            self.mute = kwargs["mute"]
        else:
            self.mute = False

    def __del__(self):
        self.delete_gurobi()

    def get_x(self):
        return self.var_x

    def get_z(self):
        return self.var_z

    @abc.abstractmethod
    def _build_variables(self):
        pass

    @abc.abstractmethod
    def _build_model(self):
        pass

    @abc.abstractmethod
    def _build_objective(self):
        pass

    @abc.abstractmethod
    def add_z_constr(self, constr):
        pass

    @abc.abstractmethod
    def solve(self):
        pass

    @abc.abstractmethod
    def init_gurobi(self):
        pass

    def delete_gurobi(self):
        if self.model is not None:
            del self.model
        if self.env is not None:
            del self.env

    def add_x_eq_constr(self, lin_expr, rhs):
        self.model.addConstr(lin_expr == rhs)
        self.m += 1

    def add_x_ineq_constr(self, lin_expr, rhs):
        self.model.addConstr(lin_expr >= rhs)
        self.l += 1

    def _eval_after_solve(self):
        x = np.zeros(self.n)
        z = np.zeros(self.n)
        for i in range(self.n):
            x[i] = self.var_x[i].x
            z[i] = self.var_z[i].x
        objval = self.model.getAttr(GRB.Attr.ObjVal)
        return z, x, objval