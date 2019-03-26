# Author:   Matthias Frey
# Date:     March 2018 - 2019

from opal.datasets.SDDSDatasetBase import *

class MemoryDataset(SDDSDatasetBase):
    
    def __init__(self, directory, fname):
        super(MemoryDataset, self).__init__(directory, fname,
                                            dataset_type='Memory usage',
                                            print_limit=11)
