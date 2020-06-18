# Copyright (c) 2017 - 2019, Matthias Frey, Paul Scherrer Institut, Villigen PSI, Switzerland
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


class ProfilingPlotter(BasePlotter):

    def __init__(self):
        pass


    def plot_lbal_histogram(self, **kwargs):
        """Particle load balancing.

        Plots the time series (i.e. simulation time) histogram with
        the number of cores having the same amount of particles.
        The user can specify ranges givin the upper and lower
        boundary, i.e. 'bupper' and, respectively, 'blower'. Those
        boundaries are given in percent.
        """
        try:
            grid     = kwargs.pop('grid', False)
            title    = kwargs.pop('title', None)
            yscale   = kwargs.pop('yscale', 'linear')
            xscale   = kwargs.pop('xscale', 'linear')
            blower   = kwargs.pop('blower', [0.0, 0.0,  25.0, 50.0, 75.0])
            bupper   = kwargs.pop('bupper', [0.0, 25.0, 50.0, 75.0, 100.0])

            if not len(blower) == len(bupper):
                raise ValueError('len(blower) != len(bupper)')

            nTotal = len(self.ds.getVariables())
            nCols = sum('processor' in var for var in self.ds.getVariables())

            time = self.ds.getData('time')

            nRows = len(time)

            # iterate through all steps and do a boxplot
            colStart = nTotal - nCols
            colEnd   = nCols + 1

            # percentages with respect to expected average number p / t
            # where p is the number of particles per processes and t the total
            # number of particles
            stamps = np.empty([nRows, len(blower)], dtype=float)

            p = 100.0 / nCols   # in percent [%]

            # each row is a time stamp
            for r in range(0, nRows):
                stamp = np.empty([nCols,], dtype=float)
                for c in range(colStart, colEnd):
                    cc = c - colStart
                    stamp[cc] = float(self.ds.getData('processor-' + str(cc))[r])
                # total number of particles
                total = sum(stamp)

                # percentage []
                stamp /= total * 0.01 # in %

                # check bin
                for i in range(0, len(blower)):

                    if blower[i] == bupper[i]:
                        stamps[r, i] = ((blower[i] <= stamp) & (stamp <= bupper[i])).sum()
                    else:
                        stamps[r, i] = ((blower[i] < stamp) & (stamp <= bupper[i])).sum()

            for i in range(0, len(blower)):

                common = str(blower[i]) + ', ' + str(bupper[i]) + '] %'
                lab = ']' + common

                if blower[i] == bupper[i]:
                    lab = '[' + common

                plt.plot(time, stamps[:, i], label=lab)


            plt.xlabel(self.ds.getLabelWithUnit('time'))
            plt.xscale(xscale)

            plt.ylabel('#cores')
            plt.yscale(yscale)

            plt.legend()

            plt.grid(grid, which='both')

            if title:
                plt.title(title)

            plt.tight_layout()

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()


    def plot_lbal_summary(self, **kwargs):
        """Particle load balancing.

        Plot the minimum, maximum and average number of
        particles per core vs. the simulation time.
        """
        try:
            grid     = kwargs.pop('grid', False)
            title    = kwargs.pop('title', None)
            yscale   = kwargs.pop('yscale', 'linear')
            xscale   = kwargs.pop('xscale', 'linear')

            nTotal = len(self.ds.getVariables())
            nCols = sum('processor' in var for var in self.ds.getVariables())


            time = self.ds.getData('time')

            nRows = len(time)

            # iterate through all steps
            colStart = nTotal - nCols
            colEnd   = nCols + 1

            # each row is a time stamp
            minimum = []
            maximum = []
            mean    = []
            for r in range(0, nRows):
                stamp = np.empty([nCols,], dtype=float)
                for c in range(colStart, colEnd):
                    cc = c - colStart
                    stamp[cc] = self.ds.getData('processor-' + str(cc))[r]
                minimum.append(min(stamp))
                mean.append(np.mean(stamp))
                maximum.append(max(stamp))

            plt.plot(time, minimum, label='minimum')
            plt.plot(time, maximum, label='maximum')
            plt.plot(time, mean, label='mean')

            plt.xlabel(self.ds.getLabelWithUnit('time'))
            plt.xscale(xscale)

            plt.ylabel('#particles')
            plt.yscale(yscale)

            plt.legend()

            plt.grid(grid, which='both')

            if title:
                plt.title(title)

            plt.tight_layout()
            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()


    def plot_lbal_boxplot(self, **kwargs):
        """Particle load balancing.

        Does a (simulation) time series boxplot of the
        particle load balancing.
        """
        try:
            grid     = kwargs.pop('grid', False)
            title    = kwargs.pop('title', None)
            yscale   = kwargs.pop('yscale', 'linear')
            xscale   = kwargs.pop('xscale', 'linear')

            nTotal = len(self.ds.getVariables())
            nCols = sum('processor' in var for var in self.ds.getVariables())

            time = self.ds.getData('time')

            nRows = len(time)

            # iterate through all steps and do a boxplot
            colStart = nTotal - nCols
            colEnd   = nCols + 1

            # each row is a time stamp
            stamps = []
            for r in range(0, nRows):
                stamp = np.empty([nCols,], dtype=float)
                for c in range(colStart, colEnd):
                    cc = c - colStart
                    stamp[cc] = float(self.ds.getData('processor-' + str(cc))[r])
                stamps.append(stamp)

            if xscale == 'log':
                # 24. Dec. 2017
                # https://stackoverflow.com/questions/19328537/check-array-for-values-equal-or-very-close-to-zero
                # https://stackoverflow.com/questions/19141432/python-numpy-machine-epsilon
                if np.any(np.absolute(time) < np.finfo(float).eps):
                    opal_logger.warning('Entry close to zero. Switching to linear x scale')
                    xscale='linear'

            plt.boxplot(stamps, 0, '', positions=time)

            plt.xlabel(self.ds.getLabelWithUnit('time'))
            plt.xscale(xscale)

            plt.ylabel('#particles')
            plt.yscale(yscale)

            plt.grid(grid, which='both')

            if title:
                plt.title(title)

            plt.tight_layout()

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()
