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


    def plot_line(self, field, step=0, **kwargs):


        ix = self.indices[:, 0]
        iy = self.indices[:, 1]
        iz = self.indices[:, 2]

        k = int(0.5 * max(iz))
        j = int(0.5 * max(iy))

        ix = ix[iz == k]
        iy = iy[iz == k]

        ix = ix[iy == j]

        x = self.positions[iz == k, 0]
        x = x[iy == j]

        ff = self.ds.getData(field, step=step)
        ff = ff[iz == k]
        ff = ff[iy == j]

        plt.plot(x, ff, **kwargs)
        return plt


    def plot_slice(self, field, normal, pos=0.0, index=0, step=0):
        """Do a slice plot.

        Parameters
        ----------
        field : str
            name of scalar field or vector field component
        normal : str
            normal direction. Either 'x', 'y', or 'z'
        pos : float, optional
            coordinate position of slice
        step : int, optional
            time step
        index : int, optional
            if index > 0, pos is ignored.

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        ix, iy, field = self.ds.getSlice(field=field,
                                         normal=normal,
                                         pos=pos,
                                         index=index,
                                         step=step)
        plt.pcolormesh(ix, iy, field)
        plt.colorbar()
        return plt

    def plot_projection(self, field, normal, step=0, method='integrated'):
        """Do a projection plot.

        Parameters
        ----------
        field : str
            name of scalar field or vector field component
        normal : str
            normal direction. Either 'x', 'y', or 'z'
        step : int, optional
            time step

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        ix, iy, values = self.ds.getSlice(field=field,
                                          normal=normal,
                                          index=1,
                                          step=step)

        xlab = 'x'
        ylab = 'y'
        if normal == 'x':
            dim = 0
            xlab = 'y'
            ylab = 'z'
        elif normal == 'y':
            dim = 1
            xlab = 'x'
            ylab = 'z'
        elif normal == 'z':
            dim = 2
            xlab = 'x'
            ylab = 'y'

        xunit = self.ds.getUnit(xlab)
        yunit = self.ds.getUnit(ylab)

        mindex = max(self.ds.indices[:, dim])

        data = self.ds.dataframe[normal].values

        dx = self.ds.get_mesh_spacing(step)[dim]

        mult = ''
        if method == 'integrated':
            mult = '*m'

        for i in range(1, int(mindex) + 1):
            _, _, data = self.ds.getSlice(field, normal, step=step, index=i)
            if method == 'integrated':
                values += data * dx
            elif method == 'sum':
                values += data
            elif method == 'max':
                values = np.maximum(values, data)
            else:
                raise ValueError("Projection method '" + method + "' not available.")

        plt.pcolormesh(ix, iy, values)
        plt.xlabel(xlab + ' [' + xunit + ']')
        plt.ylabel(ylab + ' [' + yunit + ']')
        cbar = plt.colorbar()

        clab = self.ds.getLabel(field)
        cunit = self.ds.getUnit(field)

        cbar.set_label(clab + ' [' + cunit + mult + ']')
        return plt
