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

    def plot_line(self, field, normal, step=0, **kwargs):
        """Do a line plot through the center. The line can only
        be drawn orthogonal to one of the directions x, y, or z.

        Parameters
        ----------
        field : str
            name of scalar field or vector field component
        normal : str
            normal direction. Either 'x', 'y', or 'z'
        step : int, optional
            time step
        kwargs : dict, optional
            keywords of matplotlib.pyplot.plot

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        dirs = ['x', 'y', 'z']

        if normal not in dirs:
            raise ValueError("Normal has to be one of " + str(dirs) + ".")

        idx = dirs.index(normal)

        ii = self.indices[:, (idx + 1) % 3]
        jj = self.indices[:, (idx + 2) % 3]

        i = int(0.5 * max(ii))
        j = int(0.5 * max(jj))

        jj = jj[ii == i]

        pos = self.positions[ii == i, idx]
        pos = pos[jj == j]

        ff = self.ds.getData(field, step=step)
        ff = ff[ii == i]
        ff = ff[jj == j]

        plt.plot(pos, ff, **kwargs)
        plt.xlabel(normal + ' [' + self.ds.getUnit(normal) + ']')
        plt.ylabel(self.ds.getLabel(field) + ' [' + self.ds.getUnit(field) + ']')
        return plt

    def plot_slice(self, field, normal, pos=0.0, index=0, step=0, **kwargs):
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
        kwargs : dict, optional
            keywords of matplotlib.pyplot.pcolormesh

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        ix, iy, ff = self.ds.getSlice(field=field,
                                      normal=normal,
                                      pos=pos,
                                      index=index,
                                      step=step)
        plt.pcolormesh(ix, iy, ff, **kwargs)
        cbar = plt.colorbar()
        clab = self.ds.getLabel(field)
        cunit = self.ds.getUnit(field)
        cbar.set_label(clab + ' [' + cunit + ']')

        xlab = 'x'
        ylab = 'y'
        if normal == 'x':
            xlab = 'y'
            ylab = 'z'
        elif normal == 'y':
            xlab = 'x'
            ylab = 'z'
        elif normal == 'z':
            xlab = 'x'
            ylab = 'y'

        xunit = self.ds.getUnit(xlab)
        yunit = self.ds.getUnit(ylab)

        plt.xlabel(xlab + ' [' + xunit + ']')
        plt.ylabel(ylab + ' [' + yunit + ']')

        return plt

    def plot_projection(self, field, normal, step=0, method='integrated', **kwargs):
        """Do a projection plot.

        Parameters
        ----------
        field : str
            name of scalar field or vector field component
        normal : str
            normal direction. Either 'x', 'y', or 'z'
        step : int, optional
            time step
        method : str, optional
            projection method: 'integrated', 'sum' or 'max'
        kwargs : dict, optional
            keywords of matplotlib.pyplot.pcolormesh

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

        plt.pcolormesh(ix, iy, values, **kwargs)
        plt.xlabel(xlab + ' [' + xunit + ']')
        plt.ylabel(ylab + ' [' + yunit + ']')
        cbar = plt.colorbar()

        clab = self.ds.getLabel(field)
        cunit = self.ds.getUnit(field)

        cbar.set_label(clab + ' [' + cunit + mult + ']')
        return plt
