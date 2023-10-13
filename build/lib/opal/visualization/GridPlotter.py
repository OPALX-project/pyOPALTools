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


class GridPlotter(BasePlotter):

    def __init__(self):
        pass

    def plot_grids_per_level(self, **kwargs):
        """Plot a time series of the number of grids per level
        and the total number of grids.
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

            nLevels = self.ds.getNumLevels()

            time = self.ds.getData('time')

            total = [0] * len(time)
            for l in range(nLevels):
                level = self.ds.getData('level-' + str(l))
                plt.plot(time, level, label='level ' + str(l))
                total += level

            plt.plot(time, total, label='total')
            plt.xlabel(self.ds.getLabelWithUnit('time'))
            plt.ylabel('#grids')
            plt.xscale(xscale)
            plt.yscale(yscale)
            plt.grid(grid, which='both')
            plt.tight_layout()
            plt.legend()

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()


    def plot_grid_histogram(self, **kwargs):
        """Plot a time series of the minimum, maximum and
        average number of grids per core.
        """
        try:
            hspan  = kwargs.pop('hspan', [None, None])
            grid   = kwargs.pop('grid', False)
            xscale = kwargs.pop('xscale', 'linear')
            yscale = kwargs.pop('yscale', 'linear')

            nCores= self.ds.getNumCores()

            if hspan[0] and hspan[1]:
                mingrid = hspan[0] / float(nCores)
                maxgrid = hspan[1] / float(nCores)
                # 2. Feb. 2018
                # https://stackoverflow.com/questions/23248435/fill-between-two-vertical-lines-in-matplotlib
                plt.axhspan(mingrid, maxgrid,
                            alpha=0.25, color='purple',
                            label='optimum')

            time = self.ds.getData('time')

            low  = np.asarray([np.Inf] * len(time))
            high = np.asarray([-np.Inf] * len(time))
            avg  = np.asarray([0.0] * len(time))

            for c in range(nCores):
                data = self.ds.getData('processor-' + str(c))

                low = np.minimum(low, data)
                avg += data
                high = np.maximum(high, data)

                #for j in range(len(data)):
                #    low[j] = min(low[j], data[j])
                #    avg[j] = avg[j] + data[j]
                #    high[j] = max(high[j], data[j])

            avg /= float(nCores)

            plt.plot(time, low, label='minimum')
            plt.plot(time, high, label='maximum')
            plt.plot(time, avg, label='mean')

            plt.xscale(xscale)
            plt.yscale(yscale)

            plt.xlabel(self.ds.getLabelWithUnit('time'))
            plt.ylabel('#grids per core')
            plt.grid(grid, which='both')
            plt.tight_layout()
            plt.legend()

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()
