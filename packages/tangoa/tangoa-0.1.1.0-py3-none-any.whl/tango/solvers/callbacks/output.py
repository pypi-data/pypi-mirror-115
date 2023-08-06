#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from gurobipy import GRB


def print_number_of_added_lazy_constraints(mod, where, every_ith_node=3000):
    if where == GRB.Callback.MIP:
        if not mod._mute:
            node_count = mod.cbGet(GRB.Callback.MIP_NODCNT)
            if node_count % every_ith_node == 0 and node_count > 0:
                print("Lazy constraints added: ", mod._lazy_constr_count, "of potentially",
                      mod._potential_lazy_constr_count, "many.")


def print_average_cut_off(mod, where, every_ith_node=3000):
    if where == GRB.Callback.MIP:
        if not mod._mute:
            node_count = mod.cbGet(GRB.Callback.MIP_NODCNT)
            if node_count % every_ith_node == 0 and node_count > 0:
                if len(mod._cut_offs) > 0:
                    av_cut_off = sum(mod._cut_offs) / len(mod._cut_offs)
                    print("Average cut off:", av_cut_off)
                    mod._cut_offs = []


def print_number_of_fractional_cuts_added(mod, where, every_ith_node=3000):
    if where == GRB.Callback.MIP:
        if not mod._mute:
            node_count = mod.cbGet(GRB.Callback.MIP_NODCNT)
            if node_count % every_ith_node == 0 and node_count > 0:
                print("User cuts added: ", mod._user_cuts_count)


def print_all():
    return print_number_of_added_lazy_constraints, print_number_of_fractional_cuts_added, print_average_cut_off
