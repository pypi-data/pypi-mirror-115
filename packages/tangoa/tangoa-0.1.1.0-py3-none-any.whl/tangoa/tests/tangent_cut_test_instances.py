from tangoa.solvers.tangent_cut import TangentCut
from tangoa.tests.qpsolver_test_instances import QPSolverTestInstances


class TangentCutTestInstances(QPSolverTestInstances):
    def __init__(self, failed_instances=False):
        super().__init__(failed_instances=failed_instances)

    def generate_tangent_cuts(self):
        return [TangentCut(*instance) for instance in self]