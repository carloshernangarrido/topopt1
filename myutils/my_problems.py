from abc import ABC

from topopt.problems import Problem, ElasticityProblem, ComplianceProblem


class MyProblem(Problem, ABC):
    pass


class MyElasticityProblem(ElasticityProblem, ABC):
    pass


class MyComplianceProblem(ComplianceProblem):
    pass
