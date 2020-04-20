# Copyright (c) 2018, Matthias Frey, Paul Scherrer Institut, Villigen PSI, Switzerland
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

from .DatasetBase import DatasetBase
from opal.visualization.StdOpalOutputPlotter import StdOpalOutputPlotter
from opal.analysis.StdOpalOutputAnalysis import StdOpalOutputAnalysis
import numpy as np

class StdOpalOutputDataset(DatasetBase, StdOpalOutputPlotter, StdOpalOutputAnalysis):

    def __init__(self, directory, fname):
        """Constructor.
        """
        super(StdOpalOutputDataset, self).__init__(directory, fname)

    def getData(self, var, **kwargs):
        """
        Obtain filename

        Parameters
        ----------
        var : str
            Unused

        Returns
        -------
        str
            Filename
        """
        return self.filename


    def getLabel(self, var):
        """Obtain label for plotting.

        Parameters
        ----------
        var : str
            Unused

        Returns
        -------
        str
            Empty string
        """
        return ''


    def getUnit(self, var):
        """Obtain unit for plotting.

        Parameters
        ----------
        var : str
            Unused

        Returns
        -------
        str
            Empty string
        """
        return ''

    @property
    def size(self):
        return 0
