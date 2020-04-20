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
from opal.analysis.cyclotron import \
    calcCenteringExtraction


class TrackOrbitPlotter(BasePlotter):

    def __init__(self):
        pass


    def plot_orbits(self, pid=0, **kwargs):
        """Do an orbit plot.

        Parameters
        ----------
        pid : int, optional
            Which particle id
            (default: 0)

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        try:
            xdata = self.ds.getData('x')
            ydata = self.ds.getData('y')
            ids   = self.ds.getData('ID')

            xdata = xdata[np.where(ids == pid)]
            ydata = ydata[np.where(ids == pid)]

            plt.plot(xdata, ydata, **kwargs)

            xlabel = self.ds.getLabel('x')
            xunit  = self.ds.getUnit('x')

            ylabel = self.ds.getLabel('y')
            yunit  = self.ds.getUnit('y')

            plt.xlabel(xlabel + ' [' + xunit + ']')
            plt.ylabel(ylabel + ' [' + yunit + ']')

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()


    def plot_centering(self, **kwargs):
        """

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        try:
            _, _, _, radius = self.calcTurnSeparation()

            x = calcCenteringExtraction(radius)

            plt.plot(x[2], x[3], 'o', **kwargs)

            ax = plt.gca()

            # Add circles
            circle1 = plt.Circle((0, 0), radius=2, fc='black', fill=False)
            plt.gca().add_artist(circle1)
            circle2 = plt.Circle((0, 0), radius=4, fc='black', fill=False)
            plt.gca().add_artist(circle2)

            # Move left y-axis and bottim x-axis to centre, passing through (0,0)
            ax.set_xlim(-5,5)
            ax.set_ylim(-5,5)
            ax.spines['left'].set_position('center')
            ax.spines['bottom'].set_position('center')
            # Eliminate upper and right axes
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')

            # Show ticks in the left and lower axes only
            ax.xaxis.set_ticks_position('bottom')
            ax.yaxis.set_ticks_position('left')

            plt.xlabel('E')
            plt.ylabel('F')
            ax.xaxis.set_label_coords(0.9, -0.025)
            ax.yaxis.set_label_coords(-0.025,0.9)

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()


    def plot_turns(self, **kwargs):
        """

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        try:
            _, _, _, radius = self.calcTurnSeparation()

            plt.plot(np.arange(2, len(radius)+2), radius, **kwargs) # From second turn
            plt.xlabel('Turn Number')
            plt.ylabel('Radius [m]')

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()


    def plot_energy(self, nsteps=-1, **kwargs):
        """

        Parameters
        ----------
        nsteps : int, optional
            Number of steps per turn (default -1: detect automatically)

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        try:
            _, energy, _, radius = self.calcTurnSeparation(nsteps)

            plt.xlabel('Turn Number')
            plt.ylabel('Energy [MeV]')
            # From second turn
            plt.plot(np.arange(2, len(radius)+2), energy, linewidth=2, **kwargs)
            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()


    def plot_energy_gain(self, nsteps=-1, **kwargs):
        """

        Parameters
        ----------
        nsteps : int, optional
             Number of steps per turn (default -1: detect automatically)

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        try:
            _, energy, _, radius = self.calcTurnSeparation(nsteps)

            x = np.arange(2, len(radius)+1)
            y = np.diff(energy)
            plt.xlabel('Turn Number')
            plt.ylabel('Energy Gain [MeV]')
            # From second turn
            plt.plot(x, y, linewidth=2, **kwargs)
            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()


    def plot_turn_separation(self, nsteps=-1, angle=0.0, asFunctionOfTurnNumber=True, asFunctionOfEnergy=False,**kwargs):
        """

        Parameters
        ----------
        nsteps : int, optional
            Number of steps per turn (default -1: detect automatically)
        angle : float, optional
            Angle of reference line in radians
        asFunctionOfTurnNumber : bool
            x-axis turn number
        asFunctionOfEnergy : bool
            x-axis energy

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        try:
            ts, energy, _, radius = self.calcTurnSeparation(nsteps, angle)

            if asFunctionOfTurnNumber:
                x = np.arange(2, len(ts)+2) # From second turn
                plt.xlabel('Turn Number')
            elif asFunctionOfEnergy:
                x = energy[1:] # From second turn
                plt.xlabel('Energy [MeV]')
            else:
                x = radius[1:] # From second turn, in meters
                plt.xlabel('Radius [m]')

            plt.plot(x, ts, linewidth=2, **kwargs)
            plt.ylabel('Turn Separation [m]')

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()


    def plot_beta_beat(self, nsteps=-1, **kwargs):
        """

        Parameters
        ----------
        nsteps : int, optional
            Number of steps per turn (default -1: detect automatically)

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        try:
            _, _, phi, radius = self.calcTurnSeparation(nsteps)


            angle_unit = kwargs.pop('angle_unit', 'rad')

            if 'deg' in angle_unit:
                phi = np.degrees(phi)
                angle_unit == 'deg'

            plt.plot(radius, phi, 'o-', linewidth=2, **kwargs)
            plt.xlabel('Radius [m]')
            plt.ylabel('Radial Direction [' + angle_unit + ']')

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()
