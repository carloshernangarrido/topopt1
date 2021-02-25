#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create a compliance mechanism that inverts displacments."""

# import context  # noqa

from topopt.mechanisms.my_boundary_conditions import MyDisplacementInverterBoundaryConditions
from topopt.mechanisms.problems import MechanismSynthesisProblem
from topopt.mechanisms.solvers import MechanismSynthesisSolver
from topopt.filters import SensitivityBasedFilter, DensityBasedFilter

# from topopt.guis import GUI
from myutils.my_guis import GUI

from topopt import cli


def main():
    """Run the example by constructing the TopOpt objects."""
    # Default input parameters
    nelx, nely, volfrac, penalty, rmin, ft = cli.parse_args(
        nelx=100, nely=100, volfrac=0.3, penalty=10, rmin=1.4)
    bc = MyDisplacementInverterBoundaryConditions(nelx, nely)
    # bc = GripperBoundaryConditions(nelx, nely)
    # bc = CrossSensitivityExampleBoundaryConditions(nelx, nely)
    problem = MechanismSynthesisProblem(bc, penalty)
    title = cli.title_str(nelx, nely, volfrac, rmin, penalty)
    gui = GUI(problem, title)
    filter = [SensitivityBasedFilter, DensityBasedFilter][ft](nelx, nely, rmin)
    solver = MechanismSynthesisSolver(problem, volfrac, filter, gui)
    cli.main(nelx, nely, volfrac, penalty, rmin, ft, solver=solver)


if __name__ == "__main__":
    main()





# import numpy
#
# import topopt.boundary_conditions as bcs
# import myutils.my_boundary_conditions as mbcs
#
# import topopt.guis as guis
# import myutils.my_guis as mguis
#
# import topopt.problems as problems
#
# from myutils import my_problems
#
# from topopt.solvers import TopOptSolver
# from topopt.filters import DensityBasedFilter
#
# # from input_data.lever import input_data
# from input_data.inverter import input_data
#
#
# x, rmin, volfrac, penal, nelx, nely, list_of_fixedxy, list_of_forces, dict_of_passives, dict_of_actives \
#     = input_data()
#
# bc = mbcs.MyBoundaryConditions(nelx, nely, list_of_fixedxy=list_of_fixedxy, list_of_forces=list_of_forces,
#                                dict_of_passives=dict_of_passives, dict_of_actives=dict_of_actives)
#
# # Problem to optimize given objective and constraints
# problem = my_problems.MyComplianceProblem(bc, penal, Emin=1e-9, Emax=1, nu=0.3)
# gui = mguis.GUI(problem, "Topology Optimization Example", )
# topopt_filter = DensityBasedFilter(nelx, nely, rmin)
# solver = TopOptSolver(problem, volfrac, topopt_filter, gui)
# x_opt = solver.optimize(x)
# gui.final_update()
#
# input("Press enter...")
