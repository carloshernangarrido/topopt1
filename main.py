import numpy

import topopt.boundary_conditions as bcs
import myutils.my_boundary_conditions as mbcs

import topopt.guis as guis
import myutils.my_guis as mguis

import topopt.problems as problems


from topopt.solvers import TopOptSolver
from topopt.filters import DensityBasedFilter

from input_data.lever import input_data

x, rmin, volfrac, penal, nelx, nely, list_of_fixedxy, list_of_forces, dict_of_passives, dict_of_actives = input_data()

# bc = bcs.LBracketBoundaryConditions(nelx, nely, minx=10, maxy=10)
bc = mbcs.MyBoundaryConditions(nelx, nely, list_of_fixedxy=list_of_fixedxy, list_of_forces=list_of_forces,
                               dict_of_passives=dict_of_passives, dict_of_actives=dict_of_actives)
# print(bc.active_elements)
# print(bc.passive_elements)
# print(bc.fixed_nodes)
# print(bc.forces)

# Problem to optimize given objective and constraints
problem = problems.ComplianceProblem(bc, penal)
gui = mguis.GUI(problem, "Topology Optimization Example", )
topopt_filter = DensityBasedFilter(nelx, nely, rmin)
solver = TopOptSolver(problem, volfrac, topopt_filter, gui)
x_opt = solver.optimize(x)
gui.final_update()

input("Press enter...")
