from unittest import TestCase

import numpy as np
from numpy.testing import assert_allclose

from tangoa.model_parameters import ModelParameters
from tangoa.tests.qpsolver_test_instances import QPSolverTestInstances


def lagrange_grad(x, sqrt_z, lam, mu, params):
    return (np.diag(sqrt_z) @ params.H @ np.diag(sqrt_z)) @ x + params.D @ x - np.diag(sqrt_z) @ params.b \
           - (params.A @ np.diag(sqrt_z)).transpose() @ mu - lam.transpose() @ (params.G @ np.diag(sqrt_z))


class TestQPSolver(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.instances = QPSolverTestInstances()
        cls.instance_names = cls.instances.instance_names
        cls.model_parameters = [ModelParameters(*instance) for instance in cls.instances]
        cls.solvers = cls.instances.generate_solvers()
        cls.z_collections = cls.instances.feasible_zs
        cls.fractional_z_collections = cls.instances.feasible_fractional_zs

    def test_optimal_result_is_feasible(self):
        for zs, solver, instance_name in zip(self.z_collections, self.solvers, self.instance_names):
            for z_number, z in enumerate(zs):
                with self.subTest("Test " + instance_name + " with z " + str(z_number)):
                    solver.solve(z)
                    if solver.feasible:
                        equality_constraints = solver.A @ solver.x
                        inequality_constraints = solver.G @ solver.x
                        for i in range(len(solver.w)):
                            self.assertAlmostEqual(equality_constraints[i], solver.w[i])
                        for i in range(len(solver.u)):
                            self.assertGreaterEqual(inequality_constraints[i], solver.u[i])

    def test_kkt_conditions_are_satisfied(self):
        for zs, solver, instance_name in zip(self.z_collections, self.solvers, self.instance_names):
            for z_number, z in enumerate(zs):
                with self.subTest("Test " + instance_name + " with z " + str(z_number)):
                    solver.solve(z)
                    x = solver.x
                    mu = solver.mu
                    lam = solver.lam
                    lag_grad = lagrange_grad(x, z, lam, mu, solver)
                    assert_allclose(lag_grad, np.zeros(len(x)), atol=1e-6)

    def test_kkt_conditions_are_satisfied_for_fractional_z(self):
        for zs, solver, instance_name in zip(self.fractional_z_collections, self.solvers, self.instance_names):
            for z_number, z in enumerate(zs):
                with self.subTest("Test " + instance_name + " with fractional z " + str(z_number)):
                    solver.solve(z)
                    x = solver.x
                    mu = solver.mu
                    lam = solver.lam
                    lag_grad = lagrange_grad(x, np.sqrt(np.clip(z, 0, 1)), lam, mu, solver)
                    assert_allclose(lag_grad, np.zeros(len(x)), atol=1e-6)
