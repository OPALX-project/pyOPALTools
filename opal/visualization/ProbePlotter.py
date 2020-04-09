# Copyright (c) 2019 - 2020, Matthias Frey, Paul Scherrer Institut, Villigen PSI, Switzerland
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

class ProbePlotter(BasePlotter):

    def __init__(self):
        pass


    def plot_probe_histogram(self, **kwargs):
        """Plot a histogram of the probe histogram
        bin count vs. radius.

        Parameters
        ----------
        grid : bool, optional
            Draw grid
        scale : bool, optional
            Scales to 1.0
            (default: False)
        **kwargs
            In case of H5: additional arguments
            passed to matplotlib.pyplot.hist
        bunch : int, optional
            Bunch number (default: 0)
        begin : int
            Start step (default: 0)
        end : int
            End step (default: ds.size)

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        try:
            from opal import filetype

            ylabel = self.ds.getLabel('bincount')

            if self.ds.filetype == filetype.HIST:
                bincount = self.ds.getData('bincount')
                rmin = self.ds.getData('min')
                rmax = self.ds.getData('max')
                nbins = self.ds.getData('nbins')
                #dr = self.ds.getData('binsize')

                radius = np.linspace(float(rmin), float(rmax), nbins)

                if kwargs.pop('scale', False):
                    bincount = np.asarray(bincount) / max(bincount )
                    ylabel += ' (normalized)'

                plt.grid(kwargs.pop('grid', False))

                plt.plot(radius, bincount, **kwargs)
                plt.xlabel('radius [' + self.ds.getUnit('min') + ']')
            elif self.ds.filetype == filetype.H5:
                x = []
                y = []
                bunch = kwargs.pop('bunch', -1)
                begin = kwargs.pop('begin', 0)
                end   = kwargs.pop('end', self.ds.size)
                for s in range(begin, end):
                    x.extend(self.ds.selectData(var='x', step=s, bunch=bunch))
                    y.extend(self.ds.selectData(var='y', step=s, bunch=bunch))

                plt.hist(np.hypot(x, y), **kwargs)
                plt.xlabel('radius [' + self.ds.getUnit('x') + ']')

                if kwargs.pop('density', False):
                    ylabel = 'density'

            plt.ylabel(ylabel)

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()
