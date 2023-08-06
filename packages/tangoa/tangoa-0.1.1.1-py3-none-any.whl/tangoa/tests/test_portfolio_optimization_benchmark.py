import unittest
from unittest import TestCase

import numpy as np

from tangoa.portfolio_optimization.instances import PortfolioOptimizationSyntheticInstance, \
    PortfolioOptimizationFrangioniEtAlInstance
from tangoa.portfolio_optimization.portfolio_optimization import PortfolioOptimization
from tangoa.solvers.callbacks import add_one_fractional_cut_per_ith_node
from tangoa.solvers.oa import OASolver, print_number_of_added_lazy_constraints, print_average_cut_off, \
    print_number_of_fractional_cuts_added, submit_solutions_from_lazy_callback, \
    add_lazy_constraint_if_equal_best_objective
from tangoa.solvers.perspective_solver import PerspectiveSolver


class TestPortfolioOptimizationBenchmark(TestCase):
    def test_benchmark(self):
        mv_dir = "/home/dennis/gits/combined-perspective-cuts/computational_study/portfolio_instances/frangioni_et_al/MV/"
        diagonals = "/home/dennis/gits/combined-perspective-cuts/computational_study/portfolio_instances/frangioni_et_al/diagonals/"
        inst = PortfolioOptimizationFrangioniEtAlInstance(200, "+", 1, mv_dir=mv_dir, diagonals_dir=diagonals)

        callbacks = (print_number_of_added_lazy_constraints,
                     print_average_cut_off,
                     print_number_of_fractional_cuts_added,
                     submit_solutions_from_lazy_callback,
                     add_lazy_constraint_if_equal_best_objective,
                     lambda mod, where: add_one_fractional_cut_per_ith_node(mod, where, i=1))

        s1 = PortfolioOptimization(inst.sigma, inst.mu, inst.min_return, 10, solver=OASolver, step_size=10,
                                   time_in_presolve=10)
        s1.solve()

        s2 = PortfolioOptimization(inst.sigma, inst.mu, inst.min_return, 10, solver=PerspectiveSolver)
        s2.solve()
