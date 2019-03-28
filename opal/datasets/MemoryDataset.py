# Author:   Matthias Frey
# Date:     March 2018 - 2019

from opal.datasets.SDDSDatasetBase import *
from opa.visualization.MemoryPlotter import MemoryPlotter

class MemoryDataset(SDDSDatasetBase, MemoryPlotter):
    
    def __init__(self, directory, fname):
        super(MemoryDataset, self).__init__(directory, fname,
                                            dataset_type='Memory usage',
                                            print_limit=11)
