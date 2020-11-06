# Copyright (c) 2020, Paul Scherrer Institut, Villigen PSI, Switzerland
# All rights reserved
#
# This file is part of pyOPALTools.
#
# pyOPALTools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# You should have received a copy of the GNU General Public License
# along with pyOPALTools. If not, see <https://www.gnu.org/licenses/>.

import numpy as np

class FieldAnalysis:

    def sum(self, var, step=0):
        """Get the sum of the grid data of a variable.

        Parameters
        ----------
        var : str
            variable name
        step : int, optional
            time step

        Returns
        -------
        numpy.float64
            the sum of all grid values of the given variable
        """
        data = self.ds.getData(var, step)
        return np.sum(data)

    def max(self, var, step=0):
        """Get the maximum value of a variable.

        Parameters
        ----------
        var : str
            variable name
        step : int, optional
            time step

        Returns
        -------
        numpy.float64
            the maximum value of the given variable
        """
        data = self.ds.getData(var, step)
        return np.max(data)

    def total_charge(self, step=0):
        """Get the total charge on the grid.

        Parameters
        ----------
        step : int, optional
            time step

        Returns
        -------
        numpy.float64
            the total charge on the grid
        """
        dx = self.ds.get_mesh_spacing(step)
        volume = dx[0] * dx[1] * dx[2]
        return self.sum('rho', step) * volume
