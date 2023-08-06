from unittest import TestCase

import numpy as np
from numpy.testing import assert_allclose

from tangoa.helper import gram_decomposition, to_array
from tangoa.tests.portfolio_optimization_test_instances import PortfolioOptimizationTestInstances
from tangoa.tests.utilities_for_tests import get_model_parameters, print_instance_name


class HelperOnPortfolioOptimizationTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.instances = PortfolioOptimizationTestInstances()
        cls.solvers = cls.instances.generate_solvers()
        cls.instance_names = cls.instances.instance_names

    def test_gram_decomposition1(self):
        for instance, instance_name in zip(self.instances, self.instance_names):
            with self.subTest("Test " + instance_name):
                print_instance_name(instance_name)
                Q, mu, _, _ = instance
                min_ev = min(np.linalg.eigvals(Q))
                d = [0.5 * min_ev] * len(mu)
                H, y = gram_decomposition(Q, d, mu)
                assert_allclose(H.transpose() @ H, Q - np.diag(d))
                assert_allclose(H.transpose() @ y, mu)

    def test_gram_decomposition2(self):
        for solver, instance_name in zip(self.solvers, self.instance_names):
            with self.subTest("Test " + instance_name):
                print_instance_name(instance_name)
                Q, b, c, _, A, w, _, _ = get_model_parameters(solver)
                min_ev = min(np.linalg.eigvals(Q))
                d = [0.5 * min_ev] * len(b)
                H, y = gram_decomposition(Q + 10 * A.transpose() @ A, d, b + 10 * A.transpose() @ w)
                assert_allclose(H.transpose() @ H, Q - np.diag(d) + 10 * A.transpose() @ A)
                assert_allclose(to_array(H.transpose() @ y), b + 10 * A.transpose() @ w)
