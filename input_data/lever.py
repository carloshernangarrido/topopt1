import numpy


def input_data():
    nelx, nely = 100, 50  # Number of elements in the x and y
    volfrac = 0.06  # Volume fraction for constraints
    penal = 15  # Penalty for SIMP
    rmin = 2  # Filter radius

    # Initial solution
    x = volfrac * numpy.ones(nely * nelx, dtype=float)

    # Boundary conditions defining the loads and fixed points
    list_of_fixedxy = [(round(0.25 * nelx), round(0.75 * nely), 'y'), (round(0.75 * nelx), round(0.75 * nely), 'y'),
                       (round(0.9 * nelx), round(0.5 * nely), 'xy')]

    list_of_forces = [(round(0.1 * nelx), round(0.5 * nely), 0, -1),
                      (round(0.1 * nelx), round(0.5 * nely), -0.2, -1)]  # [(x, y, fx, fy), ]

    dict_of_passives = {}  # {'min_x': 10, 'min_y': 20, 'max_x': 30, 'max_y': 40}

    dict_of_actives = {'min_x': round((0.5 - 0.009) * nelx), 'min_y': round((0.5 - 0.009) * nely),
                       'max_x': round((0.5 + 0.009) * nelx), 'max_y': round((0.5 + 0.009) * nely)}
    dict_of_actives = {}

    return x, rmin, volfrac, penal, nelx, nely, list_of_fixedxy, list_of_forces, dict_of_passives, dict_of_actives
