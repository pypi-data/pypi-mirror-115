from unittest import TestCase

from tangoa.SQUFL.squfl import SeparableQuadraticUFL
from tangoa.solvers.indicator_constraints import LogicalSolver
from tangoa.solvers.oa import OASolver
from tangoa.solvers.perspective_solver import PerspectiveSolver
from tangoa.tests.squfl_test_instances import SQUFLTestInstances
from tangoa.tests.utilities_for_tests import print_instance_name


class TestSeparableQuadraticUFL(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.instances = SQUFLTestInstances()
        cls.instance_names = cls.instances.instance_names

    def test_all_approaches_yield_the_same_optimal_value(self):
        for instance, instance_name in zip(self.instances, self.instance_names):
            with self.subTest("Test " + instance_name):
                print_instance_name(instance_name)
                outer_approximation = SeparableQuadraticUFL(*instance, solver=OASolver)
                logical_solver = SeparableQuadraticUFL(*instance, solver=LogicalSolver)
                perspective_solver = SeparableQuadraticUFL(*instance, solver=PerspectiveSolver)

                _, _, oa_objective_value = outer_approximation.solve()
                _, _, logical_objective_value = logical_solver.solve()
                _, _, perspective_objective_value = perspective_solver.solve()

                self.assertAlmostEqual(oa_objective_value, logical_objective_value, places=6)
                self.assertAlmostEqual(oa_objective_value, perspective_objective_value, places=3)
