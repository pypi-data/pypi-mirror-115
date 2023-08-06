import unittest
from unittest import TestCase

from tangoa.portfolio_optimization.portfolio_optimization import PortfolioOptimization
from tangoa.runtime import Timer
from tangoa.solvers.indicator_constraints import LogicalSolver
from tangoa.solvers.oa import OASolver
from tangoa.solvers.perspective_solver import PerspectiveSolver
from tangoa.tests.portfolio_optimization_test_instances import PortfolioOptimizationTestInstances
from tangoa.tests.utilities_for_tests import print_instance_name


class TestPortfolioOptimization(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.instances = PortfolioOptimizationTestInstances()
        cls.instance_names = cls.instances.instance_names

    def test_all_approaches_yield_the_same_optimal_value(self):
        for instance, instance_name in zip(self.instances, self.instance_names):
            with self.subTest("Test " + instance_name):
                print_instance_name(instance_name)
                outer_approximation = PortfolioOptimization(*instance, solver=OASolver)
                logical_solver = PortfolioOptimization(*instance, solver=LogicalSolver)
                perspective_solver = PortfolioOptimization(*instance, solver=PerspectiveSolver)

                _, _, oa_objective_value = outer_approximation.solve()
                _, _, logical_objective_value = logical_solver.solve()
                _, _, perspective_objective_value = perspective_solver.solve()

                self.assertAlmostEqual(oa_objective_value, logical_objective_value, places=6)
                self.assertAlmostEqual(oa_objective_value, perspective_objective_value, places=4)

    def test_all_approaches_yield_the_same_optimal_value_with_a_scalar(self):
        for instance, instance_name in zip(self.instances, self.instance_names):
            with self.subTest("Test " + instance_name):
                print_instance_name(instance_name)
                outer_approximation = PortfolioOptimization(*instance, solver=OASolver, objective_scalar=1e4)
                logical_solver = PortfolioOptimization(*instance, solver=LogicalSolver, objective_scalar=1e4)
                perspective_solver = PortfolioOptimization(*instance, solver=PerspectiveSolver, objective_scalar=1e4)

                _, _, oa_objective_value = outer_approximation.solve()
                _, _, logical_objective_value = logical_solver.solve()
                _, _, perspective_objective_value = perspective_solver.solve()

                self.assertAlmostEqual(oa_objective_value, logical_objective_value, places=6)
                self.assertAlmostEqual(oa_objective_value, perspective_objective_value, places=4)

    def test_all_approaches_yield_the_same_optimal_value_with_a_warmstart(self):
        for instance, instance_name in zip(self.instances, self.instance_names):
            with self.subTest("Test " + instance_name):
                print_instance_name(instance_name)
                logical_solver = PortfolioOptimization(*instance, solver=LogicalSolver, objective_scalar=1e4)
                z, _, logical_objective_value = logical_solver.solve()

                outer_approximation = PortfolioOptimization(*instance, solver=OASolver, warmstart=z)
                perspective_solver = PortfolioOptimization(*instance, solver=PerspectiveSolver, warmstart=z)

                _, _, oa_objective_value = outer_approximation.solve()
                _, _, perspective_objective_value = perspective_solver.solve()

                self.assertAlmostEqual(oa_objective_value, logical_objective_value, places=6)
                self.assertAlmostEqual(oa_objective_value, perspective_objective_value, places=4)

    def test_time_limit_works(self):
        for instance, instance_name in zip(self.instances, self.instance_names):
            with self.subTest("Test " + instance_name):
                print_instance_name(instance_name)
                outer_approximation = PortfolioOptimization(*instance, solver=OASolver, time_limit=1)
                timer = Timer()
                timer.start()
                outer_approximation.solve()
                timer.stop()
                self.assertLessEqual(timer.elapsed_time, 3)

    def run_failed_instance(self, i):
        failed_instances = PortfolioOptimizationTestInstances(failed_instances=True)
        instance = failed_instances[i]
        instance_name = failed_instances.instance_names[i]
        print_instance_name(instance_name)
        solver = PortfolioOptimization(*instance, **failed_instances.additional_kwargs[instance_name])
        solver.solve()

    # @unittest.SkipTest
    def test_failed_experiments1(self):
        self.run_failed_instance(0)

    def test_failed_experiments2(self):
        self.run_failed_instance(1)

    def test_failed_experiments3(self):
        self.run_failed_instance(2)
