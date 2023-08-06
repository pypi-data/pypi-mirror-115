#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from gurobipy import GRB
import numpy as np

from tangoa.solvers.callbacks.fractional_cuts_utils import get_relaxation_values


def add_fractional_cut_if_cutoff_big_enough(mod, where, cutoff=0.5):
    if where == GRB.Callback.MIPNODE:
        if mod.cbGet(GRB.Callback.MIPNODE_STATUS) not in (3, 6):
            obj_bound = mod.cbGet(GRB.Callback.MIPNODE_OBJBND)
            best_obj = mod.cbGet(GRB.Callback.MIPNODE_OBJBST)

            eta, z = get_relaxation_values(mod)

            mod._tangent_cut.compute(z, mod._params.d)
            val = mod._tangent_cut.support
            if mod._objective_scalar * abs(val - eta) / abs(best_obj - obj_bound) > cutoff:
                mod.cbCut(mod._tangent_cut.get_cut(mod._var_eta, mod._var_z))


def add_one_fractional_cut_per_ith_node(mod, where, i=10):
    if where == GRB.Callback.MIPNODE:
        if mod.cbGet(GRB.Callback.MIPNODE_STATUS) not in (3, 6):
            if not hasattr(mod, "_node_cut_dict"):
                mod._node_cut_dict = set()
            node_count = mod.cbGet(GRB.Callback.MIPNODE_NODCNT)
            if node_count % i == 0:
                if not node_count in mod._node_cut_dict:
                    mod._node_cut_dict.add(node_count)
                    eta, z = get_relaxation_values(mod)
                    mod._tangent_cut.compute(z, mod._params.d)
                    mod.cbCut(mod._tangent_cut.get_cut(mod._var_eta, mod._var_z))
                    mod._user_cuts_count += 1


def add_fractional_cuts_only_in_root_node(where, mod, cutoff=0.1):
    node_count = mod.cbGet(GRB.Callback.MIPNODE_NODCNT)
    if node_count == 0:
        add_fractional_cut_if_cutoff_big_enough(where, mod, cutoff=cutoff)
