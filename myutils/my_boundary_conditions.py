from abc import ABC

import numpy
from topopt.boundary_conditions import BoundaryConditions, xy_to_id


class MyExtendedBoundaryConditions(BoundaryConditions, ABC):
    """
    A class used to extend BoundaryConditions class originally builtin within topopt.boundary_conditions.
    It adds 2 public methods to convert forces and fized dofs.

    ...

    Attributes
    ----------
    inherited from topopt.boundary_conditions.BoundaryConditions

    Methods
    -------
    fxy2f(fxy)
        Forces at coordinates to forces at dof ids

    fixedxy2fixed(fixedxy)
        Fixed dofs at coordinates to fixed dofs at dof ids
    """

    def fxy2f(self, fxy: list) -> numpy.ndarray:
        """ Forces at coordinates to forces at dof ids

        Converts a list of tuples as [(x1, y1, fx1, fy1), (x2, y2, fx2, fy2), ...]
        to a numpy.ndarray suitable to specify forces.

        Parameters
        ----------
        fxy : list
            list of 4-tuples as [(x1, y1, fx1, fy1), (x2, y2, fx2, fy2), ...]

        Returns
        -------
        numpy.ndarray
            numpy.ndarray with shape = (ndofs, 1), where ndofs = 2 * ((nelx+1) * (nely + 1))
        """

        f = numpy.zeros((self.ndof, 1))
        for item in fxy:
            x_ = item[0]
            y_ = item[1]
            fx_ = item[2] if item[2] else 0
            fy_ = item[3] if item[3] else 0
            f[xy_to_id(x_, y_, self.nelx, self.nely) * 2, 0] = fx_
            f[xy_to_id(x_, y_, self.nelx, self.nely) * 2 + 1, 0] = fy_
        return f

    def fixedxy2fixed(self, fixedxy: list) -> numpy.ndarray:
        """ Fixed dofs at coordinates to fixed dofs at dof ids

            Converts a list of tuples as [(x1, y1, x_y_1), (x2, y2, x_y_2), ...]
            to a numpy.ndarray suitable to specify fixed dofs.

            Parameters
            ----------
            fixedxy : list
                list of 3-tuples as [(x1, y1, x_y_1), (x2, y2, x_y_2), ...]
                x_y_1 = 'x' <-> fixed along x at x1, y1
                x_y_1 = 'y' <-> fixed along y at x1, y1
                x_y_1 = 'xy' <-> fixed along x and y at x1, y1

            Returns
            -------
            numpy.ndarray
                numpy.ndarray with shape = (ndofs, 1), where ndofs = 2 * ((nelx+1) * (nely + 1))
            """

        fixed_list = []
        for item in fixedxy:
            x_ = item[0]
            y_ = item[1]
            x_y_ = item[2]
            if x_y_ == 'x':
                fixed_list.append(xy_to_id(x_, y_, self.nelx, self.nely) * 2)
            elif x_y_ == 'y':
                fixed_list.append(xy_to_id(x_, y_, self.nelx, self.nely) * 2 + 1)
            elif x_y_ == 'xy':
                fixed_list.append(xy_to_id(x_, y_, self.nelx, self.nely) * 2)
                fixed_list.append(xy_to_id(x_, y_, self.nelx, self.nely) * 2 + 1)
            else:
                raise ValueError
        return numpy.array(fixed_list)


class MyBoundaryConditions(MyExtendedBoundaryConditions):
    """Customizable Boundary conditions"""
    def __init__(self, nelx, nely, list_of_fixedxy, list_of_forces, dict_of_passives, dict_of_actives):
        super().__init__(nelx, nely)
        self.list_of_fixedxy = list_of_fixedxy
        self.list_of_forces = list_of_forces
        try:
            self.passive_min_x = dict_of_passives['min_x']
            self.passive_max_x = dict_of_passives['max_x']
            self.passive_min_y = dict_of_passives['min_y']
            self.passive_max_y = dict_of_passives['max_y']
        except KeyError:
            self.passive_min_x = None
            self.passive_max_x = None
            self.passive_min_y = None
            self.passive_max_y = None
        try:
            self.active_min_x = dict_of_actives['min_x']
            self.active_max_x = dict_of_actives['max_x']
            self.active_min_y = dict_of_actives['min_y']
            self.active_max_y = dict_of_actives['max_y']
        except KeyError:
            self.active_min_x = None
            self.active_max_x = None
            self.active_min_y = None
            self.active_max_y = None


    @property
    def fixed_nodes(self):
        """:obj:`numpy.ndarray`: Fixed nodes."""
        # dofs = numpy.arange(self.ndof)
        # fixed = numpy.union1d(dofs[0:2 * (self.nely + 1):2], numpy.array(
        #     [2 * (self.nelx + 1) * (self.nely + 1) - 1]))

        # list_of_fixedxy = [(0, i_y, 'x') for i_y in range(self.nely+1)] + \
        #                   [(self.nelx, self.nely, 'y')] + \
        #                   [(self.nelx // 2, self.nely, 'y')]

        fixed = self.fixedxy2fixed(self.list_of_fixedxy)
        return fixed

    @property
    def forces(self):
        """:obj:`numpy.ndarray`: Force vector."""
        # list_of_forces = [(round(self.nelx/2), 2, 1, -1),  # (x, y, fx, fy)
        #                   ]
        # list_of_forces = [(round(0.4*self.nelx), round(0.5*self.nely),  1, 0),  # (x, y, fx, fy)
        #                   (round(0.9*self.nelx), round(1*self.nely), -1, 0), ]
        f = self.fxy2f(self.list_of_forces)
        return f

    @property
    def passive_elements(self):
        """:obj:`numpy.ndarray`: Passive elements in the upper right corner."""
        if self.passive_min_x is None:
            return numpy.array([])
        X, Y = numpy.mgrid[self.passive_min_x:self.passive_max_x + 1,
                           self.passive_min_y:self.passive_max_y + 1]
        pairs = numpy.vstack([X.ravel(), Y.ravel()]).T
        passive_to_ids = numpy.vectorize(lambda xy: xy_to_id(
            *xy, nelx=self.nelx - 1, nely=self.nely - 1), signature="(m)->()")
        return passive_to_ids(pairs)

    @property
    def active_elements(self):
        """:obj:`numpy.ndarray`: Passive elements in the upper right corner."""
        if self.active_min_x is None:
            return numpy.array([])
        X, Y = numpy.mgrid[self.active_min_x:self.active_max_x + 1,
                           self.active_min_y:self.active_max_y + 1]
        pairs = numpy.vstack([X.ravel(), Y.ravel()]).T
        active_to_ids = numpy.vectorize(lambda xy: xy_to_id(
            *xy, nelx=self.nelx - 1, nely=self.nely - 1), signature="(m)->()")
        return active_to_ids(pairs)
