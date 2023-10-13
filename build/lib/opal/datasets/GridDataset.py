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

from opal.datasets.SDDSDatasetBase import *
from opal.visualization.GridPlotter import GridPlotter

class GridDataset(SDDSDatasetBase, GridPlotter):

    def __init__(self, directory, fname):
        """
        """
        vmapper = {
            'time': 't'
        }

        umapper = [
            'time'
        ]
        super(GridDataset, self).__init__(directory, fname,
                                          variable_mapper=vmapper,
                                          unit_label_mapper=umapper,
                                          dataset_type='Grid',
                                          print_limit=11)


    def getNumLevels(self):
        """Obtain the number of levels.

        Returns
        -------
        int
        """
        variables = super(GridDataset, self).getVariables()
        return sum('level-' in var for var in variables)


    def getNumCores(self):
        """Obtain the number of cores.

        Returns
        -------
        int
        """
        variables = super(GridDataset, self).getVariables()
        return sum('processor-' in var for var in variables)
