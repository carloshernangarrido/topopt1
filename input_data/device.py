import numpy


def input_data():
    nelx, nely = 500, 500  # Number of elements in the x and y
    volfrac = 0.1 # Volume fraction for constraints
    penal = 10  # Penalty for SIMP
    rmin = 2  # Filter radius

    # Initial solution
    x = volfrac * numpy.ones(nely * nelx, dtype=float)

    # Boundary conditions defining the loads and fixed points
    list_of_fixedxy = [(round(x_frac * nelx), round(0.0 * nely), 'y')
                       for x_frac in numpy.arange(start=0.0, stop=0.5, step=1/nely)]  # support
    simmetry = [(round(0.0 * nelx), round(y_frac * nely), 'x')
                for y_frac in numpy.arange(start=0.0, stop=1.0, step=1/nely)]  # simmetry

    list_of_fixedxy = list_of_fixedxy + simmetry

    list_of_forces = [(round(x_frac * nelx), round(1.0 * nely), 0, 1)
                      for x_frac in numpy.arange(start=0.0, stop=0.5, step=1/nely)]  # [(x, y, fx, fy), ]

    dict_of_passives = {'min_x': round(0.0 * nelx), 'min_y': round(0.65 * nely),
                        'max_x': round(0.1 * nelx), 'max_y': round(0.80 * nely)}
    dict_of_passives = {}

    dict_of_actives = {'min_x': round(0.00 * nelx), 'min_y': round(0.0 * nely),
                       'max_x': round(0.5 * nelx), 'max_y': 0}

    return x, rmin, volfrac, penal, nelx, nely, list_of_fixedxy, list_of_forces, dict_of_passives, dict_of_actives
