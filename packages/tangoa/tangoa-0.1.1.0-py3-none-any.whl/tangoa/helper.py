#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from numpy.linalg import svd, solve
import numpy as np
from scipy.sparse import diags, issparse


def nonzeros(z, tol=1e-8):
    subset = []
    for i, elem in enumerate(z):
        if abs(elem) > tol:
            subset.append(i)
    return subset


def gram_decomposition(Q, d, b):
    u, s, v = svd(Q - np.diag(d))
    H = np.diag(np.sqrt(s)) @ u.transpose()
    y = solve(H.transpose(), b)
    return H, y


def to_binary(z):
    return np.around(np.clip(z, 0, 1))


def diag(d):
    return diags(d, 0, format="csr")


def as_vector(v):
    v.shape = (len(v), 1)


def to_array(v):
    if isinstance(v, np.ndarray) and len(v.shape) == 1:
        return v
    elif issparse(v):
        return np.ravel(v.todense())
    else:
        return np.ravel(v)


def as_scalar(v):
    if isinstance(v, np.matrix) or isinstance(v, np.ndarray):
        return v.item()
    else:
        return v


def is_binary(z):
    np.allclose(z, np.around(z))
