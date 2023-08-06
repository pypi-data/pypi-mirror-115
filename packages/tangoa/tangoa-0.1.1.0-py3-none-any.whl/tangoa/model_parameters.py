#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import numpy as np
from scipy.sparse import issparse

from tangoa.helper import diag, as_vector


def check_args(*args):
    if len(args) < 4:
        raise RuntimeError("4 arguments are required. " + str(len(args)) + " are given.")


def check_con_integrity(A, w, G, u):
    equality_cons = False
    if (A is not None) and (w is not None):
        if len(w) != A.shape[0]:
            raise RuntimeError("A and w do not have matching dimensions.")
        equality_cons = True
    inequality_cons = False
    if (G is not None) and (u is not None):
        if len(u) != G.shape[0]:
            raise RuntimeError("G and u do not have matching dimensions.")
        inequality_cons = True
    return equality_cons, inequality_cons


def check_kwargs(**kwargs):
    essential_keys = (
        "Q", "b", "c", "d"
    )
    for k in essential_keys:
        if k not in kwargs.keys():
            raise RuntimeError(str(k) + " is not provided.")


class ObjectiveParameters:
    def __init__(self, *args, **kwargs):
        self.objective_scalar = 1.0
        if len(args) == 1:
            if isinstance(args[0], ObjectiveParameters):
                self.Q = args[0].Q
                self.b = args[0].b
                self.c = args[0].c
                self.d = args[0].d
                self.objective_scalar = args[0].objective_scalar
            else:
                raise RuntimeError("Argument must be an ObjectiveParameters or a ModelParameters object.")
        elif len(args) >= 4:
            self.Q, self.b, self.c, self.d = args[:4]
        elif len(args) == 0:
            check_kwargs(**kwargs)
            self.Q = kwargs["Q"]
            self.b = kwargs["b"]
            self.c = kwargs["c"]
            self.d = kwargs["d"]
        else:
            raise RuntimeError("Not the right number of arguments given.")
        self.D = diag(self.d)
        self.H = self.Q - self.D
        if not issparse(self.H):
            if isinstance(self.H, np.matrix):
                self.H = np.asarray(self.H)
        self.n = len(self.b)

        if "objective_scalar" in kwargs.keys():
            self.objective_scalar = kwargs["objective_scalar"]

    def get_args(self):
        return self.Q, self.b, self.c, self.d


class ModelParameters(ObjectiveParameters):
    def __init__(self, *args, A=None, w=None, G=None, u=None, **kwargs):
        super().__init__(*args, **kwargs)
        if len(args) == 1:
            if isinstance(args[0], ModelParameters):
                self.A = args[0].A
                self.w = args[0].w
                self.G = args[0].G
                self.u = args[0].u
                self.equality_cons = args[0].equality_cons
                self.inequality_cons = args[0].inequality_cons
                self.objective_scalar = args[0].objective_scalar
            else:
                raise RuntimeError("Argument must be a Parameters object.")
        elif len(args) == 0:
            check_kwargs(**kwargs)
            self.A = A
            self.w = w
            self.G = G
            self.u = u
            self.equality_cons, self.inequality_cons = check_con_integrity(self.A, self.w, self.G, self.u)
        elif len(args) == 4:
            self.A = A
            self.w = w
            self.G = G
            self.u = u
            self.equality_cons, self.inequality_cons = check_con_integrity(self.A, self.w, self.G, self.u)
        elif len(args) == 8:
            self.A, self.w, self.G, self.u = args[4:8]
            self.equality_cons, self.inequality_cons = check_con_integrity(self.A, self.w, self.G, self.u)
        else:
            raise RuntimeError("Not the right number of arguments given.")
        if self.equality_cons:
            self.m = len(self.w)
        else:
            self.m = 0
        if self.inequality_cons:
            self.l = len(self.u)
        else:
            self.l = 0

        if "objective_scalar" in kwargs.keys():
            self.objective_scalar = kwargs["objective_scalar"]

    def get_kwargs(self):
        return {
            "A": self.A,
            "w": self.w,
            "G": self.G,
            "u": self.u,
            "objective_scalar": self.objective_scalar
        }
