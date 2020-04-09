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

from .TimingPlotter import *
import numpy as np


class StdOpalOutputPlotter(TimingPlotter):

    def __init__(self):
        pass


    def plot_RF_phases(self, RFcavity, **kwargs):
        """

        Parameters
        ----------
        RFcavity : list [str]
            List of names of the RFcavity as specifed in the input file

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        try:
            data = self.calcRFphases(RFcavity)

            for i, cname in enumerate(RFcavity):
                turns  = data[i][0]
                phases = data[i][1]
                plt.plot(turns, phases, linewidth=3, label=cname, **kwargs)
            plt.xlabel("Turn number")
            plt.ylabel("RF phase [deg]")
            plt.legend(loc=0)

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()
