import random

import numpy as np

from tangoa.portfolio_optimization.instances import PortfolioOptimizationSyntheticInstance
from tangoa.portfolio_optimization.portfolio_optimization import PortfolioOptimization
from tangoa.solvers.oa import OASolver
from tangoa.solvers.perspective_solver import PerspectiveSolver


def draw_z(n, k, seed):
    np.random.seed(seed)
    random.seed(seed)

    subset = random.sample(list(range(n)), k)

    z = np.zeros(n)
    for i in subset:
        z[i] = 1

    return z


def draw_fractional_z(n, k, seed):
    z = np.zeros(n)
    np.random.seed(seed)
    while sum(z) < k:
        z = (z + np.random.rand(n))
        if sum(z) >= k:
            z = z / sum(z) * k
    return z


class PortfolioOptimizationTestInstances:
    def __init__(self, failed_instances=False):
        if failed_instances:
            self.instances = [
                PortfolioOptimizationSyntheticInstance(100, 100, 0.05, 0.01, 29958838),
                PortfolioOptimizationSyntheticInstance(100, 1, 0.05, 0.01, 29958838),
                PortfolioOptimizationSyntheticInstance(100, 10, 0.05, 0.01, 3356886)
            ]
            self.ks = [
                40,
                20,
                40
            ]
            self.feasible_zs = [[], []]
            self.feasible_fractional_zs = [[], []]
            self.instance_names = [
                "FAILEDPERSPECTIVE100_1",
                "FAILEDPERSPECTIVE100_2",
                "FAILEDPERSPECTIVE100_3"
            ]
            self.additional_kwargs = {
                "FAILEDPERSPECTIVE100_1":
                    {
                        "solver": PerspectiveSolver,
                        "time_limit": 30
                    },
                "FAILEDPERSPECTIVE100_2":
                    {
                        "solver": PerspectiveSolver,
                        "time_limit": 30
                    },
                "FAILEDPERSPECTIVE100_3":
                    {
                        "solver": PerspectiveSolver,
                        "time_limit": 30
                    }
            }
        else:
            self.instances = [
                PortfolioOptimizationSyntheticInstance(10, 10, 0.05, 0.01, 413524),
                PortfolioOptimizationSyntheticInstance(20, 5, 0.01, 0.01, 1324),
                PortfolioOptimizationSyntheticInstance(20, 10, 0.01, 0.01, 132134)
            ]

            self.ks = [
                6,
                12,
                15
            ]

            self.feasible_zs = [
                [draw_z(10, 6, seed) for seed in (2132, 1345, 65, 31)],
                [draw_z(20, 12, seed) for seed in (213132, 45, 42, 45345)],
                [draw_z(20, 15, seed) for seed in (31, 65, 24, 7566, 1453, 64)]
            ]
            self.feasible_fractional_zs = [
                [draw_fractional_z(10, 6, seed) for seed in (22, 14321, 1235, 311)],
                [draw_fractional_z(20, 12, seed) for seed in (23412, 1324, 14323312, 31432)],
                [draw_fractional_z(20, 15, seed) for seed in (223, 11, 1232455, 332141)]]

            self.instance_names = [
                "PO10",
                "PO20",
                "PO30"
            ]

    @staticmethod
    def __extract_instance(instance, k):
        return instance.sigma, instance.mu, instance.min_return, k

    def __getitem__(self, item):
        return self.__extract_instance(self.instances[item], self.ks[item])

    def __iter__(self):
        for instance, k in zip(self.instances, self.ks):
            yield self.__extract_instance(instance, k)

    def __len__(self):
        return len(self.instances)

    def generate_solvers(self, solver=OASolver):
        return [PortfolioOptimization(*args, solver=solver) for args in self]
