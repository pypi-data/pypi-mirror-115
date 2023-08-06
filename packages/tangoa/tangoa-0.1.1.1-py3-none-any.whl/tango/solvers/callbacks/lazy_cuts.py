#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from tangoa.solvers.callbacks.lazy_cut_utils import add_lazy_constraint
from gurobipy import GRB


def always_add_lazy_constraint(mod, where):
    if where == GRB.Callback.MIPSOL:
        curr_obj = mod.cbGet(GRB.Callback.MIPSOL_OBJ)
        mod._potential_lazy_constr_count += 1
        add_lazy_constraint(curr_obj, mod)


def add_lazy_constraint_if_equal_best_objective(mod, where):
    if where == GRB.Callback.MIPSOL:
        best_obj = mod.cbGet(GRB.Callback.MIPSOL_OBJBST)
        curr_obj = mod.cbGet(GRB.Callback.MIPSOL_OBJ)
        mod._potential_lazy_constr_count += 1
        if abs(curr_obj - best_obj) < 1e-8:
            add_lazy_constraint(curr_obj, mod)
