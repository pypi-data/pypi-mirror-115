from unittest import TestCase

from tangoa.model_parameters import ModelParameters
from tangoa.objectives import phi, psi_bar, perspective_objective_value
from tangoa.tests.portfolio_optimization_test_instances import PortfolioOptimizationTestInstances
from tangoa.tests.qpsolver_test_instances import QPSolverTestInstances
from tangoa.tests.squfl_test_instances import SQUFLTestInstances
from tangoa.tests.utilities_for_tests import get_relaxation_solver, print_instance_name


class Test(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        high_level_solvers = PortfolioOptimizationTestInstances().generate_solvers() + \
                             SQUFLTestInstances().generate_solvers()
        cls.instances = QPSolverTestInstances()
        cls.model_parameters = [ModelParameters(*instance) for instance in cls.instances]
        cls.solvers = cls.instances.generate_solvers()
        cls.z_collections = cls.instances.feasible_zs
        cls.fractional_z_collections = cls.instances.feasible_fractional_zs
        cls.perspective_relaxation_solvers = [get_relaxation_solver(solver) for solver in high_level_solvers]
        cls.instance_names = cls.instances.instance_names

    def test_if_phi_runs_without_errors(self):
        for zs, solver, instance_name in zip(self.z_collections, self.solvers, self.instance_names):
            for i, z in enumerate(zs):
                print_instance_name(instance_name)
                with self.subTest(msg="Test " + instance_name + " with z" + str(i)):
                    print_instance_name(instance_name + " with z" + str(i))
                    solver.solve(z)
                    phi(solver.x, z, *solver.get_args())

    def test_if_psi_runs_without_errors(self):
        for zs, solver, instance_name in zip(self.z_collections, self.solvers, self.instance_names):
            for i, z in enumerate(zs):
                with self.subTest(msg="Test " + instance_name + " with z" + str(i)):
                    print_instance_name(instance_name + " with z" + str(i))
                    psi_bar(z, *solver.get_args(), **solver.get_kwargs())

    def test_function_perspective_objective_value_is_the_same_as_real_perspective_value(self):
        for relaxation, qp_solver, instance_name in zip(self.perspective_relaxation_solvers, self.solvers,
                                                        self.instance_names):
            with self.subTest(msg="Test " + instance_name):
                print_instance_name(instance_name)
                rel_z, rel_x, rel_val = relaxation.solve()
                qp_solver.solve(rel_z)
                x = qp_solver.x
                val = perspective_objective_value(x, rel_z, relaxation)
                # Seems like numerical difficulties make it necessary to put the tolerance that high
                self.assertAlmostEqual(rel_val, val, places=3)

    def test_psi_bar_is_the_same_as_the_perspective_value(self):
        for relaxation, model_parameters, instance_name in zip(self.perspective_relaxation_solvers,
                                                               self.model_parameters, self.instance_names):
            with self.subTest(msg="Test " + instance_name):
                print_instance_name(instance_name)
                rel_z, rel_x, rel_val = relaxation.solve()
                val = psi_bar(rel_z, model_parameters)
                # Seems like numerical difficulties make it necessary to put the tolerance that high
                self.assertAlmostEqual(rel_val, val, places=3)
