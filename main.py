import numpy
import topopt.boundary_conditions as bcs

import myutils.my_boundary_conditions as mbcs
import topopt.problems as problems
from topopt.solvers import TopOptSolver
from topopt.filters import DensityBasedFilter
import myutils.my_guis as mguis

nelx, nely = 100, 50  # Number of elements in the x and y
volfrac = 0.2  # Volume fraction for constraints
penal = 15  # Penalty for SIMP
rmin = 2  # Filter radius

# Initial solution
x = volfrac * numpy.ones(nely * nelx, dtype=float)

# Boundary conditions defining the loads and fixed points
# list_of_fixedxy = [(i_x, nely, 'y') for i_x in range(1, nelx, 45)] + \
#                   [(i_x, nely, 'x') for i_x in range(1, nelx, 45)]  # + [(0, i_y, 'x') for i_y in range(nely + 1)] \

list_of_fixedxy = [(round(0.5 * nelx), round(0.25 * nely), 'y'),
                   (round(0.5 * nelx), round(0.75 * nely), 'y'),
                   (round(0.1 * nelx), round(0.5 * nely), 'xy')]

list_of_forces = [(round(0.9 * nelx), round(0.5 * nely), 1, 0)]  # [(x, y, fx, fy), ]

dict_of_passives = {}  # {'min_x': 10, 'min_y': 20, 'max_x': 30, 'max_y': 40}

dict_of_actives = {'min_x': round((0.5 - 0.009) * nelx), 'min_y': round((0.5 - 0.009) * nely),
                   'max_x': round((0.5 + 0.009) * nelx), 'max_y': round((0.5 + 0.009) * nely)}
dict_of_actives = {}


bc = bcs.LBracketBoundaryConditions(nelx, nely, minx=10, maxy=10)
# bc = mbcs.MyBoundaryConditions(nelx, nely, list_of_fixedxy=list_of_fixedxy, list_of_forces=list_of_forces,
#                                dict_of_passives=dict_of_passives, dict_of_actives=dict_of_actives)
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
