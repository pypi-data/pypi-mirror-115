from unittest import TestCase

import numpy as np
from numpy.testing import assert_allclose

from tangoa.model_parameters import ObjectiveParameters, ModelParameters


class TestParameters(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        np.random.seed(42)
        X = np.random.random((10, 3))
        cls.Q = X.transpose() @ X
        cls.b = np.random.random(3)
        cls.n = len(cls.b)
        cls.c = np.random.random(3)
        min_ev = min(np.linalg.eigvals(cls.Q))
        cls.d = [min_ev] * cls.n
        cls.A = np.random.random((2, 3))
        cls.w = np.random.random(2)
        cls.G = np.eye(3)
        cls.u = np.zeros(3)

    def test_all_objective_parameter_constructors_should_result_in_the_same_data(self):
        params1 = ObjectiveParameters(self.Q, self.b, self.c, self.d)
        params2 = ObjectiveParameters(Q=self.Q, b=self.b, c=self.c, d=self.d)
        params3 = ObjectiveParameters(params1)

        assert_allclose(self.Q, params1.Q)
        assert_allclose(self.b, params1.b)
        assert_allclose(self.c, params1.c)
        assert_allclose(self.d, params1.d)

        def assert_params_are_equal(first_params, second_params):
            for attribute in ("Q", "b", "c", "d"):
                assert_allclose(getattr(first_params, attribute), getattr(second_params, attribute))

        assert_params_are_equal(params1, params2)
        assert_params_are_equal(params1, params3)

    def test_all_model_parameter_constructors_should_result_in_the_same_data(self):
        params1 = ModelParameters(self.Q, self.b, self.c, self.d, self.A, self.w, self.G, self.u)
        params2 = ModelParameters(self.Q, self.b, self.c, self.d, A=self.A, w=self.w, G=self.G, u=self.u)
        params3 = ModelParameters(Q=self.Q, b=self.b, c=self.c, d=self.d, A=self.A, w=self.w, G=self.G, u=self.u)
        params4 = ModelParameters(params1)

        assert_allclose(self.Q, params1.Q)
        assert_allclose(self.b, params1.b)
        assert_allclose(self.c, params1.c)
        assert_allclose(self.d, params1.d)
        assert_allclose(self.A, params1.A)
        assert_allclose(self.w, params1.w)
        assert_allclose(self.G, params1.G)
        assert_allclose(self.u, params1.u)

        def assert_params_are_equal(first_params, second_params):
            for attribute in ("Q", "b", "c", "d", "A", "w", "G", "u"):
                assert_allclose(getattr(first_params, attribute), getattr(second_params, attribute))

        assert_params_are_equal(params1, params2)
        assert_params_are_equal(params1, params3)
        assert_params_are_equal(params1, params4)
