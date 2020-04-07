# Author:   Matthias Frey
# Date:     March 2018 - 2019

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
