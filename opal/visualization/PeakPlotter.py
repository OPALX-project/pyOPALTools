# Copyright (c) 2019, Matthias Frey, Paul Scherrer Institut, Villigen PSI, Switzerland
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
import os


class PeakPlotter(BasePlotter):

    def __init__(self):
        pass


    def plot_peak_difference(self, dset, **kwargs):
        """Plot the peak difference of a probe output.

        Parameters
        ----------
        dset : PeakDataset
            A dataset
        grid : bool, optional
            Draw grid
        raxis : bool, optional
            Do radius vs radius plot instead
        begin : int, optional
            First peak
        end : int, optional
            Last peak

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        try:
            if isinstance(dset, list):
                raise ValueError('Exactly 1 datasets expected. ' +
                                'len(dsets) = ' + str(len(dset)) + ' != 1.')

            dsets = [self.ds, dset]

            for ds in dsets:
                from opal import filetype
                if not ds.filetype == filetype.PEAK:
                    raise TypeError(ds.filename +
                                    ' is not a peak (*.peaks) file.')

            unit = dsets[0].getUnit('radius')

            if not unit == dsets[1].getUnit('radius'):
                raise ValueError('Not same radius units.')

            peaks1 = dsets[0].getData('radius')
            peaks2 = dsets[1].getData('radius')

            npeaks = min(len(peaks1), len(peaks2))
            begin = kwargs.pop('begin', 0)
            end   = kwargs.pop('end', npeaks)

            if begin < 0:

                opal_logger.error("Invalid parameter value 'begin = " + str(begin) + "'")

            if end < begin or end > npeaks:

                opal_logger.error("Invalid parameter value 'end = " + str(end) + "'")

            p1 = peaks1[begin:end]
            p2 = peaks2[begin:end]

            npeaks = len(p2)

            plt.grid(kwargs.pop('grid', False))
            radiusPlot = kwargs.pop('raxis', False)

            if radiusPlot:
                lowest  = min(min(p1), min(p2))
                highest = max(max(p1), max(p2))

                plt.plot([lowest, highest], [lowest, highest],
                        linestyle='dashed', color='black',
                        label='y = x')

                plt.plot(p1, p2, marker='o', **kwargs)

                plt.xlabel(self.ds.getLabelWithUnit('radius') + ' (' +
                           os.path.basename(dsets[0].filename) + ')')
                plt.ylabel(self.ds.getLabelWithUnit('radius') + ' (' +
                           os.path.basename(dsets[1].filename) + ')')
            else:
                diff = p1 - p2

                xticks = range(begin, end)

                plt.plot(xticks, diff, 'o', **kwargs)

                plt.xlabel('peak number')

                plt.ylabel('peak difference [' + unit + ']')

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()
