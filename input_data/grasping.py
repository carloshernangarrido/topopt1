import numpy


def input_data():
    nelx, nely = 100, 100  # Number of elements in the x and y
    volfrac = 0.1 # Volume fraction for constraints
    penal = 10  # Penalty for SIMP
    rmin = 2  # Filter radius

    # Initial solution
    x = volfrac * numpy.ones(nely * nelx, dtype=float)

    # Boundary conditions defining the loads and fixed points
    list_of_fixedxy = [(round(0.1 * nelx), round(0.75 * nely), 'x'),
                       (round(0.1 * nelx), round(0.70 * nely), 'xy'),
                       ]
    simmetry = [(round(0.0 * nelx), round(y_frac * nely), 'x')
                for y_frac in numpy.arange(start=0.5, stop=1.0, step=1/nely)]  # simmetry

    list_of_fixedxy = list_of_fixedxy + simmetry

    list_of_forces = [(round(0.25 * nelx), round(0.25 * nely), -1, 0.1)]  # [(x, y, fx, fy), ]

    dict_of_passives = {'min_x': round(0.0 * nelx), 'min_y': round(0.65 * nely),
                        'max_x': round(0.1 * nelx), 'max_y': round(0.80 * nely)}

    dict_of_actives = {'min_x': round(0.1 * nelx), 'min_y': round(0.65 * nely),
                       'max_x': round(0.2 * nelx), 'max_y': round(0.80 * nely)}


    return x, rmin, volfrac, penal, nelx, nely, list_of_fixedxy, list_of_forces, dict_of_passives, dict_of_actives
