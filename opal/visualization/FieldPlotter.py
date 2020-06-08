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

from .BasePlotter import *
import numpy as np

class FieldPlotter(BasePlotter):

    def __init__(self):
        pass

    def plot_slice(self, field, normal, pos=0.0, index=0, step=0):
        """Do a slice plot.

        Parameters
        ----------
        field : str
            name of scalar field or vector field component
        normal : str
            normal direction. Either 'x', 'y', or 'z'
        pos : float
            coordinate position of slice
        step : int
            time step
        index : int
            optional to 'pos'. If index > 0, pos is ignored.

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        ix, iy, field = self.ds.getSlice(field, normal, pos, step, index=index)
        plt.pcolormesh(ix, iy, field)
        plt.colorbar()
        return plt

    def plot_projection(self, field, normal, step=0):
        """Do a projection plot.

        Parameters
        ----------
        field : str
            name of scalar field or vector field component
        normal : str
            normal direction. Either 'x', 'y', or 'z'
        step : int
            time step
        index : int
            optional to 'pos'. If index > 0, pos is ignored.

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        ix, iy, field_sum = self.ds.getSlice(field, normal, step=step, index=1)

        xlab = 'x'
        ylab = 'y'
        xunit = self.ds.getUnit('x')
        yunit = self.ds.getUnit('y')
        if normal == 'x':
            dim = 0
            xlab = 'y'
            ylab = 'z'
            xunit = self.ds.getUnit('y')
            yunit = self.ds.getUnit('z')
        elif normal == 'y':
            dim = 1
            xlab = 'x'
            ylab = 'z'
            xunit = self.ds.getUnit('x')
            yunit = self.ds.getUnit('z')
        elif normal == 'z':
            dim = 2

        mindex = max(self.ds.indices[:, dim])

        data = self.ds.dataframe[normal].values

        # mesh spacing in each dimension is constant in OPAL
        # --> it is enough to take just one value
        dx = np.diff(data)[0]

        for i in range(1, int(mindex) + 1):
            _, _, data = self.ds.getSlice(field, normal, step=step, index=i)
            field_sum += data * dx
        plt.pcolormesh(ix, iy, field_sum)
        plt.xlabel(xlab + ' [' + xunit + ']')
        plt.ylabel(ylab + ' [' + yunit + ']')
        cbar = plt.colorbar()

        clab = self.ds.getLabel(field)
        cunit = self.ds.getUnit(field)

        cbar.set_label(clab + ' [' + cunit + '*m]')
        return plt
