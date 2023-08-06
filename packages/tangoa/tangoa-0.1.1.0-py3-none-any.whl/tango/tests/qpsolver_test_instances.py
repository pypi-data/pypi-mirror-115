from tangoa.solvers.subsolvers.GurobiQPSolver import GurobiQPSolver
from tangoa.tests.portfolio_optimization_test_instances import PortfolioOptimizationTestInstances
from tangoa.tests.squfl_test_instances import SQUFLTestInstances
from tangoa.tests.utilities_for_tests import get_model_parameters


class QPSolverTestInstances:
    def __init__(self, failed_instances=False):
        portfolio_instances = PortfolioOptimizationTestInstances(failed_instances=failed_instances)
        squfl_instances = SQUFLTestInstances(failed_instances=failed_instances)

        self.high_level_solvers = portfolio_instances.generate_solvers() + squfl_instances.generate_solvers()

        self.instances = [get_model_parameters(solver) for solver in self.high_level_solvers]
        self.feasible_zs = portfolio_instances.feasible_zs
        self.feasible_zs += squfl_instances.feasible_zs
        self.feasible_fractional_zs = portfolio_instances.feasible_fractional_zs
        self.feasible_fractional_zs += squfl_instances.feasible_fractional_zs
        self.instance_names = portfolio_instances.instance_names + squfl_instances.instance_names

    def __iter__(self):
        for instance in self.instances:
            yield instance

    def __len__(self):
        return len(self.instances)

    def __getitem__(self, item):
        return self.instances[item]

    def generate_solvers(self):
        return [GurobiQPSolver(*instance) for instance in self]
