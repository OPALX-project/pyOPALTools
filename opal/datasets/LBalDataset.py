# Author:   Matthias Frey
# Date:     March 2018 - 2019

from opal.datasets.SDDSDatasetBase import *

class LBalDataset(SDDSDatasetBase):
    
    def __init__(self, directory, fname):
        vmapper = {
            'time':         't'
        }
        
        umapper = [
            'time'
        ]
        
        super(LBalDataset, self).__init__(directory, fname,
                                          variable_mapper=vmapper,
                                          unit_label_mapper=umapper,
                                          dataset_type='Load balancing',
                                          print_limit=11)
