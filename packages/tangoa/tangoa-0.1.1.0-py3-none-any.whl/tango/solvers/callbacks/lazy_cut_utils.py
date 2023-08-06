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

# from tangoa.solvers.d_optimizer.minimal_difference import MinimalDifference
from tangoa.helper import to_binary
from tangoa.solvers.tangent_cut import TangentCut


def add_lazy_constraint(curr_obj, mod):
    # Get values of variables
    eta = mod.cbGetSolution(mod._var_eta)
    z_dict = mod.cbGetSolution(mod._var_z)
    z = np.zeros(len(mod._params.b))
    for i in range(len(mod._params.b)):
        z[i] = z_dict[i]
    z = to_binary(z)

    # Optimize d
    # if mod._sdp_per_lazy_constr and mod.cbGet(GRB.Callback.MIPSOL_NODCNT) == 0.0:
    #     print("Optimizing lazy constraint via SDP...")
    #     diff = MinimalDifference(mod._params.Q, mod._params.b, mod._params.A, mod._params.w, 1e-4)
    #     d, diff_val = diff.solve(z)
    # else:
    d = mod._params.d

    # Determine cut
    mod._tangent_cut.just_run_qp_solver(z, d)
    val = mod._tangent_cut.support

    # if mod._params.objective_scalar * val > eta - 1e-4:
    mod._tangent_cut.compute(z, d, do_not_call_solver=True)
    mod._cut_offs.append(mod._params.objective_scalar * val - eta)
    constr = mod._tangent_cut.get_cut(mod._var_eta, mod._var_z)
    mod.cbLazy(constr)
    mod._zs_to_submit.append(z)
    mod._etas_to_submit.append(mod._params.objective_scalar * val)
    mod._lazy_constr_count += 1
