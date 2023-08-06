#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import numpy as np
from numpy.random import *


class SQUFLInstance:
    def __init__(self, n_facilities, n_costumers, seed=None):
        self.seed = seed
        self.Q = None
        self.c = None

        self.generate(n_facilities, n_costumers)

    def generate(self, n_facilities, n_costumers):
        if self.seed is not None:
            seed(self.seed)
        f_x = uniform(0, 1, n_facilities)
        f_y = uniform(0, 1, n_facilities)
        f = np.zeros((n_facilities, 2))
        for i in range(n_facilities):
            f[i, 0] = f_x[i]
            f[i, 1] = f_y[i]
        co_x = uniform(0, 1, n_costumers)
        co_y = uniform(0, 1, n_costumers)
        co = np.zeros((n_costumers, 2))
        for j in range(n_costumers):
            co[j, 0] = co_x[j]
            co[j, 1] = co_y[j]
        self.Q = np.zeros((n_facilities, n_costumers))
        for i in range(n_facilities):
            for j in range(n_costumers):
                self.Q[i, j] = 50 * np.linalg.norm(f[i, :] - co[j, :], 2)
        self.c = uniform(1, 100, n_facilities)
