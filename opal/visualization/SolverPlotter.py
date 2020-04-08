# Copyright (c) 2018 - 2019, Matthias Frey, Paul Scherrer Institut, Villigen PSI, Switzerland
# All rights reserved
#
# Implemented as part of the PhD thesis
# "Precise Simulations of Multibunches in High Intensity Cyclotrons"
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


class SolverPlotter(BasePlotter):

    def __init__(self):
        pass

    def plot_solver_histogram(self, var, **kwargs):
        """Plot a time series of solver output, e.g. error,
        number of iterations, etc.
        """
        try:
            hspan  = kwargs.pop('hspan', [None, None])
            grid   = kwargs.pop('grid', False)
            xscale = kwargs.pop('xscale', 'linear')
            yscale = kwargs.pop('yscale', 'linear')

            if hspan[0] and hspan[1]:
                plt.axhspan(hspan[0], hspan[1],
                            alpha=0.25, color='purple',
                            label='[' + str(hspan[0]) + ', ' + str(hspan[1]) +']')

            time = self.ds.getData('time')
            data = self.ds.getData(var)
            plt.plot(time, data)

            plt.xlabel(self.ds.getLabel('time') + ' [' + self.ds.getUnit('time') + ']')

            if self.ds.getUnit(var) == r'$1$':
                plt.ylabel(self.ds.getLabel(var))
            else:
                print ( self.ds.getUnit(var) )
                plt.ylabel(self.ds.getLabel(var) + ' [' + self.ds.getUnit(var) + ']')

            plt.grid(grid, which='both')
            plt.xscale(xscale)
            plt.yscale(yscale)
            plt.tight_layout()
            plt.legend()

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()
