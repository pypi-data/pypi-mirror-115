import unittest
from unittest import TestCase

import gurobipy as gp
from gurobipy import GRB
from numpy.testing import assert_allclose
from scipy.optimize import approx_fprime

from tangoa.helper import to_array
from tangoa.model_parameters import ModelParameters
from tangoa.objectives import psi_bar
from tangoa.solvers.tangent_cut import TangentCut
from tangoa.tests.portfolio_optimization_test_instances import PortfolioOptimizationTestInstances
from tangoa.tests.squfl_test_instances import SQUFLTestInstances
from tangoa.tests.tangent_cut_test_instances import TangentCutTestInstances
from tangoa.tests.utilities_for_tests import print_instance_name


def general_coef(i, Q, b, d, A, G, subsolver, sz):
    qp = to_array(Q[:, i].copy())
    qp[i] -= d[i]
    v = b[i] - (qp.transpose() @ np.diag(sz)).dot(subsolver.x)
    if A is not None:
        v += A[:, i].transpose().dot(subsolver.mu)
    if G is not None:
        v += G[:, i].transpose().dot(subsolver.lam)
    s = (v ** 2).item()
    return s


class Test(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.instances = TangentCutTestInstances()
        cls.model_parameters = [ModelParameters(*instance) for instance in cls.instances]
        cls.tangent_cuts = cls.instances.generate_tangent_cuts()
        cls.qp_solvers = cls.instances.generate_solvers()
        cls.perspective_relaxations = [high_level_solver.solver.relaxation for high_level_solver in
                                       cls.instances.high_level_solvers]
        cls.z_collections = cls.instances.feasible_zs
        cls.fractional_z_collections = cls.instances.feasible_fractional_zs
        cls.instance_names = cls.instances.instance_names

    def test_coefs_same_with_different_computations(self):
        for tangent_cut, solver, zs, instance_name in zip(self.tangent_cuts, self.qp_solvers, self.z_collections,
                                                          self.instance_names):
            for i, z in enumerate(zs):
                with self.subTest("Test " + instance_name + " with z " + str(i)):
                    print_instance_name(instance_name + " with z " + str(i))
                    n = tangent_cut.n
                    tangent_cut.compute(z)
                    from_coefs = -2.0 * tangent_cut.coefs
                    solver.solve(z)
                    for i in range(n):
                        from_general_formula = general_coef(i, solver.Q, solver.b, solver.d,
                                                            solver.A, solver.G,
                                                            solver, np.sqrt(z)) / solver.d[i]
                        if z[i] > 1e-6:
                            from_specialized_formula = solver.d[i] * tangent_cut.delta(i, z)
                        else:
                            from_specialized_formula = tangent_cut.gamma(i, np.sqrt(z)) / solver.d[i]
                        self.assertAlmostEqual(from_general_formula, from_specialized_formula, places=5)
                        self.assertAlmostEqual(from_general_formula, from_coefs[i], places=5)

    def test_coefs_same_with_different_computation_for_fractional_values(self):
        for tangent_cut, solver, zs, instance_name in zip(self.tangent_cuts, self.qp_solvers,
                                                          self.fractional_z_collections,
                                                          self.instance_names):
            for i, z in enumerate(zs):
                with self.subTest("Test " + instance_name + " with fractional z " + str(i)):
                    print_instance_name(instance_name + " with fractional z " + str(i))
                    n = tangent_cut.n
                    tangent_cut.compute(z)
                    from_coefs = -2.0 * tangent_cut.coefs
                    solver.solve(z)
                    clipped_z = np.clip(z, 0, 1)
                    for i in range(n):
                        from_general_formula = general_coef(i, solver.Q, solver.b, solver.d,
                                                            solver.A, solver.G,
                                                            solver, np.sqrt(clipped_z)) / solver.d[i]
                        if z[i] > 1e-6:
                            from_specialized_formula = solver.d[i] * tangent_cut.delta(i, clipped_z)
                        else:
                            from_specialized_formula = tangent_cut.gamma(i, np.sqrt(clipped_z)) / solver.d[i]
                        self.assertAlmostEqual(from_general_formula, from_specialized_formula, places=5)
                        self.assertAlmostEqual(from_general_formula, from_coefs[i], places=7)

    def test_small_perturbations_around_cut_support_are_still_feasible(self):
        np.random.seed(42)
        for tangent_cut, zs, model_parameters, instance_name in zip(self.tangent_cuts, self.z_collections,
                                                                    self.model_parameters, self.instance_names):
            n = model_parameters.n
            for i, z in enumerate(zs):
                with self.subTest("Test " + instance_name + " with z " + str(i)):
                    print_instance_name(instance_name + " with z " + str(i))
                    tangent_cut.compute(z)
                    for _ in range(10):
                        perturbation = 1e-3 * np.random.random(n)
                        perturbated_z = z.copy()
                        for k in range(n):
                            if perturbated_z[k] == 1:
                                perturbated_z[k] -= perturbation[k]
                            else:
                                perturbated_z[k] += perturbation[k]
                        val = psi_bar(perturbated_z, model_parameters)
                        rhs = tangent_cut.support
                        for k in range(n):
                            rhs += tangent_cut.coefs[k] * (perturbated_z[k] - z[k]) + tangent_cut.c[k] * (
                                    perturbated_z[k] - z[k])
                        self.assertGreaterEqual(val, rhs)

    def test_for_all_zs_that_tangent_cuts_are_valid(self):
        for tangent_cut, zs, model_parameters, instance_name in zip(self.tangent_cuts, self.z_collections,
                                                                    self.model_parameters, self.instance_names):
            n = model_parameters.n
            for i, z in enumerate(zs):
                with self.subTest("Test " + instance_name + " with z " + str(i)):
                    print_instance_name(instance_name + " with z " + str(i))
                    tangent_cut.compute(z)
                    for z_to_check in zs:
                        val = psi_bar(z_to_check, model_parameters)
                        rhs = tangent_cut.support
                        for k in range(n):
                            rhs += tangent_cut.coefs[k] * (z_to_check[k] - z[k]) + tangent_cut.c[k] * (
                                    z_to_check[k] - z[k])
                        self.assertGreaterEqual(val, rhs)

    def test_vectorized_coefficient_computation(self):
        for tangent_cut, zs, model_parameters, instance_name in zip(self.tangent_cuts, self.z_collections,
                                                                    self.model_parameters, self.instance_names):
            n = model_parameters.n
            for i, z in enumerate(zs):
                with self.subTest("Test " + instance_name + " with z " + str(i)):
                    print_instance_name(instance_name + " with z " + str(i))
                    sz = np.sqrt(np.clip(z, 0, 1))

                    tangent_cut.just_run_qp_solver(z)
                    coefficients_computed_vectorized = tangent_cut._compute_coefs(z)
                    coefficients_computed_pointwise = np.zeros(n)
                    for k in range(n):
                        if abs(z[k]) > 1e-8:
                            coefficients_computed_pointwise[k] = -0.5 * model_parameters.d[k] * tangent_cut.delta(k, sz)
                        else:
                            coefficients_computed_pointwise[k] = -tangent_cut.gamma(k, sz) / (
                                    2.0 * model_parameters.d[k])
                    assert_allclose(coefficients_computed_pointwise, coefficients_computed_vectorized, atol=1e-6)

    def test_support_same_as_relaxation_value(self):
        for tangent_cut, zs, perspective_relaxation, instance_name in zip(self.tangent_cuts, self.z_collections,
                                                                          self.perspective_relaxations,
                                                                          self.instance_names):
            for i, z in enumerate(zs):
                with self.subTest("Test " + instance_name + " with z " + str(i)):
                    print_instance_name(instance_name + " with z " + str(i))
                    relaxed_z, relaxed_x, relaxation_value = perspective_relaxation.solve()
                    tangent_cut.compute(relaxed_z)
                    self.assertAlmostEqual(relaxation_value, tangent_cut.support, places=3)

    def test_optimizing_squfl_after_root_cut_do_not_allow_better_value(self):
        instances = SQUFLTestInstances()
        high_level_solvers = instances.generate_solvers()
        instance_names = instances.instance_names
        model_parameter_collection = [high_level_solver.solver.get_model_parameters() for high_level_solver in
                                      high_level_solvers]
        tangent_cuts = [TangentCut(model_parameters) for model_parameters in model_parameter_collection]
        perspective_relaxations = [high_level_solver.solver.relaxation for high_level_solver in high_level_solvers]
        for tangent_cut, high_level_solver, perspective_relaxation, instance_name in zip(tangent_cuts,
                                                                                         high_level_solvers,
                                                                                         perspective_relaxations,
                                                                                         instance_names):
            with self.subTest("Test " + instance_name):
                print_instance_name(instance_name)

                n = high_level_solver.n
                n_facilities = high_level_solver.n_facilities
                n_customers = high_level_solver.n_customers

                model = gp.Model("root_cut_test")

                var_z = model.addVars(range(n), lb=0, ub=1)
                var_eta = model.addVar(lb=-float("inf"))

                for i in range(n_facilities):
                    for j in range(n_customers - 1):
                        model.addConstr(var_z[n_customers * i + j] == var_z[n_customers * i + j + 1])

                relaxed_z, relaxed_x, relaxation_value = perspective_relaxation.solve()
                tangent_cut.compute(relaxed_z)

                model.addConstr(tangent_cut.get_cut(var_eta, var_z),
                                name="Best relaxation cut")

                model.setObjective(var_eta)
                model.optimize()
                objective_value = model.getAttr(GRB.Attr.ObjVal)
                self.assertAlmostEqual(objective_value, relaxation_value, places=1)

    def test_optimizing_po_after_root_cut_do_not_allow_better_value(self):
        instances = PortfolioOptimizationTestInstances()
        high_level_solvers = instances.generate_solvers()
        instance_names = instances.instance_names
        model_parameter_collection = [high_level_solver.solver.get_model_parameters() for high_level_solver in
                                      high_level_solvers]
        tangent_cuts = [TangentCut(model_parameters) for model_parameters in model_parameter_collection]
        perspective_relaxations = [high_level_solver.solver.relaxation for high_level_solver in high_level_solvers]
        for tangent_cut, high_level_solver, perspective_relaxation, instance_name in zip(tangent_cuts,
                                                                                         high_level_solvers,
                                                                                         perspective_relaxations,
                                                                                         instance_names):
            n = high_level_solver.n
            with self.subTest("Test " + instance_name):
                print_instance_name(instance_name)
                model = gp.Model("root_cut_test")

                var_z = model.addVars(range(n), lb=0, ub=1)
                var_eta = model.addVar(lb=-float("inf"))

                model.addConstr(gp.quicksum([var_z[i] for i in range(n)]) == high_level_solver.k)

                relaxed_z, relaxed_x, relaxation_value = perspective_relaxation.solve()
                tangent_cut.compute(relaxed_z)

                model.addConstr(tangent_cut.get_cut(var_eta, var_z),
                                name="Best relaxation cut")

                model.setObjective(var_eta)
                model.optimize()

                objective_value = model.getAttr(GRB.Attr.ObjVal)
                self.assertAlmostEqual(objective_value, relaxation_value, places=1)

    @unittest.SkipTest
    def test_gradient_is_equal_to_approximative_gradient_at_integer_points(self):
        for tangent_cut, zs, perspective_relaxation, instance_name in zip(self.tangent_cuts, self.z_collections,
                                                                          self.perspective_relaxations,
                                                                          self.instance_names):
            for i, z in enumerate(zs):
                with self.subTest("Test " + instance_name + " with z " + str(i)):
                    print_instance_name(instance_name + " with z " + str(i))
                    approximative_gradient = approx_fprime(z, lambda z: psi_bar(z, tangent_cut), epsilon=1e-8)
                    tangent_cut.compute(z)
                    gradient = tangent_cut.coefs
                    for k in range(len(gradient)):
                        gradient += tangent_cut.c[k]
                    np.allclose(gradient, approximative_gradient)

    @unittest.SkipTest
    def test_gradient_is_equal_to_approximative_gradient_at_fractional_points(self):
        for tangent_cut, zs, perspective_relaxation, instance_name in zip(self.tangent_cuts,
                                                                          self.fractional_z_collections,
                                                                          self.perspective_relaxations,
                                                                          self.instance_names):
            for i, z in enumerate(zs):
                with self.subTest("Test " + instance_name + " with z " + str(i)):
                    print_instance_name(instance_name + " with z " + str(i))
                    approximative_gradient = approx_fprime(z, lambda z: psi_bar(z, tangent_cut), epsilon=1e-8)
                    tangent_cut.compute(z)
                    gradient = tangent_cut.coefs
                    for k in range(len(gradient)):
                        gradient += tangent_cut.c[k]
                    np.allclose(gradient, approximative_gradient)
