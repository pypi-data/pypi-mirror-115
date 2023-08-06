import random

import numpy as np

from tangoa.SQUFL.instances import SQUFLInstance
from tangoa.SQUFL.squfl import SeparableQuadraticUFL


def draw_squfl_z(n_facilities, n_customers, seed):
    np.random.seed(seed)
    random.seed(seed)
    n = n_facilities * n_customers

    card = np.random.randint(1, n_facilities)
    s = random.sample(list(range(n_facilities)), card)

    z = np.zeros(n)
    for i in s:
        for j in range(n_customers):
            z[n_customers * i + j] = 1

    return z


class SQUFLTestInstances:
    def __init__(self, failed_instances=False):
        if failed_instances:
            self.instances = []
            self.feasible_zs = []
            self.feasible_fractional_zs = []
            self.instance_names = []
        else:
            self.instances = [
                SQUFLInstance(2, 5, 42),
                SQUFLInstance(20, 100, 12321)
            ]
            self.feasible_zs = [
                [draw_squfl_z(2, 5, seed) for seed in (431243, 3123, 5425, 654362)],
                [draw_squfl_z(20, 100, seed) for seed in (132413, 513463, 1542, 13, 3543, 56)]
            ]
            self.feasible_fractional_zs = []
            self.instance_names = [
                "SQUFL2_5",
                "SQUFL20_100"
            ]

    def __getitem__(self, item):
        return self.instances[item].Q, self.instances[item].c

    def __iter__(self):
        for instance in self.instances:
            yield instance.Q, instance.c

    def __len__(self):
        return len(self.instances)

    def generate_solvers(self):
        return [SeparableQuadraticUFL(*args) for args in self]
