from unittest import TestCase
import itertools
from numpy.testing import assert_allclose

from tangoa.portfolio_optimization.instances import PortfolioOptimizationSyntheticInstance, \
    PortfolioOptimizationFrangioniEtAlInstance


class TestPortfolioOptimizationInstance(TestCase):
    def test_with_same_seed_same_instance_is_generated(self):
        instance1 = PortfolioOptimizationSyntheticInstance(100, 1, 0.01, 0.01, seed=1)
        instance2 = PortfolioOptimizationSyntheticInstance(100, 1, 0.01, 0.01, seed=1)

        assert_allclose(instance1.sigma, instance2.sigma)
        assert_allclose(instance2.mu, instance2.mu)
        self.assertAlmostEqual(instance1.min_return, instance2.min_return)

    def test_frangioni_et_al_instance(self):
        sizes = (200, 300, 400)
        diagonal_dominances = ("+", "0", "-")
        instance_numbers = list(range(10))
        for size, diagonal_dominance, instance_number in itertools.product(sizes, diagonal_dominances,
                                                                           instance_numbers):
            instance = PortfolioOptimizationFrangioniEtAlInstance(size, diagonal_dominance, instance_number,
                                                                  "/home/dennis/gits/combined-perspective-cuts/computational_study/portfolio_instances/frangioni_et_al/MV/",
                                                                  "/home/dennis/gits/combined-perspective-cuts/computational_study/portfolio_instances/frangioni_et_al/diagonals/")
