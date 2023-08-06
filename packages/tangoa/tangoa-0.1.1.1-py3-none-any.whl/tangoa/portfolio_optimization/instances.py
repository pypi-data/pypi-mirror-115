#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import math
import os

import numpy as np
from scipy.stats import norm


class PortfolioOptimizationFrangioniEtAlInstance:
    def __init__(self, n, diagonal_dominance, instance_number, mv_dir, diagonals_dir):
        """

        Args:
            n: Instance size. Either 200, 300 or 400.
            diagonal_dominance: String with either '+', '0' or '-'.
            instance_number: The number of the instance
            mv_dir: Must be the MV directory from http://groups.di.unipi.it/optimize/Data/MV.html
            diagonals_dir: Must be the diagonals directory from http://groups.di.unipi.it/optimize/Data/MV.html
        """
        self.n = n
        self.diagonal_dominance = diagonal_dominance
        self.instance_number = instance_number
        self.mv_dir = mv_dir
        if self.mv_dir[-1] != "/":
            self.mv_dir += "/"
        self.diagonals_dir = diagonals_dir
        if self.diagonals_dir[-1] != "/":
            self.diagonals_dir += "/"
        self.__assert_input()

        self.sigma = None
        self.mu = None
        self.min_return = None
        self.x_lower_bounds = None
        self.x_upper_bounds = None
        self.d = None

        self.__load_instance()

    def __load_instance(self):
        sigma_path, mu_path, rho_path, bounds_path, d_path = self.__get_instance_file_paths()
        self.sigma = self.__load_sigma(sigma_path)
        self.mu = self.__load_mu(mu_path)
        self.min_return = self.__load_min_return(rho_path)
        self.x_lower_bounds, self.x_upper_bounds = self.__load_bounds(bounds_path)
        self.d = self.__load_d(d_path)

    def __get_instance_file_paths(self):
        mu_path, rho_path, sigma_path, bounds_path = self.__build_mv_file_paths()
        d_path = self.__build_diagonals_file_path()
        return sigma_path, mu_path, rho_path, bounds_path, d_path

    def __build_instance_string(self):
        instance_string = ""
        if self.diagonal_dominance == "+":
            instance_string += "pard" + str(self.n) + "_"
        elif self.diagonal_dominance == "0" and self.n == 200:
            instance_string += "orl" + str(self.n) + "-05-"
        elif self.diagonal_dominance == "0" and self.n != 200:
            instance_string += "orl" + str(self.n) + "_05_"
        elif self.diagonal_dominance == "-" and self.n == 200:
            instance_string += "orl" + str(self.n) + "-005-"
        elif self.diagonal_dominance == "-" and self.n != 200:
            instance_string += "orl" + str(self.n) + "_005_"
        instance_string += chr(97 + self.instance_number)
        return instance_string

    def __build_diagonals_file_path(self):
        return self.diagonals_dir + "l-n/" + self.__build_instance_string() + ".diag"

    def __build_mv_file_paths(self):
        instance_file_path = self.mv_dir + "size" + str(self.n) + "/" + self.__build_instance_string()
        mu_path = instance_file_path + ".txt"
        rho_path = instance_file_path + ".rho"
        sigma_path = instance_file_path + ".mat"
        bounds_path = instance_file_path + ".bds"
        return mu_path, rho_path, sigma_path, bounds_path

    def __assert_input(self):
        assert self.n in (200, 300, 400), "n must be either 200, 300 or 400."
        assert self.diagonal_dominance in ("+", "0", "-"), "diagonal_dominance must be either '+', '0' or '-'."
        assert os.path.isdir(self.mv_dir), self.mv_dir + " is not a directory."
        assert os.path.isdir(self.mv_dir + "size200/"), "No folder " + self.mv_dir + "size200/ found but required."
        assert os.path.isdir(self.mv_dir + "size300/"), "No folder " + self.mv_dir + "size300/ found but required."
        assert os.path.isdir(self.mv_dir + "size400/"), "No folder " + self.mv_dir + "size400/ found but required."
        assert os.path.isdir(self.diagonals_dir)
        assert os.path.isdir(
            self.diagonals_dir + "l-n/"), "No folder " + self.diagonals_dir + "l-n/ found but required."

    @staticmethod
    def __load_sigma(sigma_path):
        with open(sigma_path) as f:
            return np.loadtxt(f, skiprows=1)

    @staticmethod
    def __load_mu(mu_path):
        with open(mu_path) as f:
            return np.loadtxt(f, skiprows=1)[:, 0]

    @staticmethod
    def __load_min_return(rho_path):
        with open(rho_path) as f:
            return float(f.readline())

    @staticmethod
    def __load_d(d_path):
        with open(d_path) as f:
            return np.loadtxt(f, skiprows=1)

    @staticmethod
    def __load_bounds(bounds_path):
        with open(bounds_path) as f:
            bounds_as_matrix = np.loadtxt(f)
            return bounds_as_matrix[:, 0], bounds_as_matrix[:, 1]



class PortfolioOptimizationSyntheticInstance:
    def __init__(self, n, e_bar, e, v, seed=None):
        self.seed = seed

        self.sigma = None
        self.mu = None
        self.min_return = None

        self.generate(n, e_bar, e, v)

    def _compute_sigma_mu(self, n, e, v, e_bar):
        m = max(1, round((e_bar * e_bar - e * e) / v))
        e_hat = np.sqrt(e / m)
        v_hat = - math.pow(e_hat, 2) + np.sqrt(math.pow(e_hat, 4) + (v / m))

        u = np.random.uniform(0, 1, (n, m))

        q = norm.ppf(u)
        f = e_hat + np.sqrt(v_hat) * q

        # q = np.zeros((n, m))
        # f = np.zeros((n, m))
        # for i in range(n):
        #     for j in range(m):
        #         q[i, j] = norm.ppf(u[i, j])
        #         f[i, j] = e_hat + np.sqrt(v_hat) * q[i, j]
        sigma = f @ f.transpose()
        mu = np.random.uniform(0.02, high=0.1, size=n)
        sigma = sigma.astype(float)
        return sigma, mu

    def generate(self, n, e_bar, e, v):
        # Set seed
        if self.seed is not None:
            np.random.seed(self.seed)
        self.sigma, self.mu = self._compute_sigma_mu(n, e, v, e_bar)
        self.min_return = np.random.uniform(0.002, 0.01)
