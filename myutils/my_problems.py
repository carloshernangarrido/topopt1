from abc import ABC

from topopt.boundary_conditions import BoundaryConditions
from topopt.problems import Problem, ElasticityProblem, ComplianceProblem


class MyProblem(Problem, ABC):
    pass


class MyElasticityProblem(ElasticityProblem, MyProblem):
    """Extends class problems.ElasticityProblem in such a way that Emin, Emax and nu are customizable
    """

    def __init__(self, bc: BoundaryConditions, penalty: float, Emin=None, Emax=1.0, nu=0.3):
        """
        Create the topology optimization problem.

        Parameters
        ----------
        bc:
            The boundary conditions of the problem.
        penalty:
            The penalty value used to penalize fractional densities in SIMP.
        Emin: float
        The Young's modulus use for the void regions.
    Emax: float
        The Young's modulus use for the solid regions.
    nu: float
        Poisson's ratio of the material.

        """
        super(MyElasticityProblem, self).__init__(bc, penalty)
        # Max and min stiffness, and Poisson's ratio
        self.nu = nu
        self.Emax = Emax
        if Emin is None:
            self.Emin = 1e-9 * Emax
        else:
            self.Emin = Emin
        print(self.Emin)
        print(self.Emax)


class MyComplianceProblem(ComplianceProblem, MyElasticityProblem):
    pass
