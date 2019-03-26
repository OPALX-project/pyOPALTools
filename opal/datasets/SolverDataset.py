# Author:   Matthias Frey
# Date:     March 2018 - 2019

from opal.datasets.SDDSDatasetBase import *

class SolverDataset(SDDSDatasetBase):
    
    def __init__(self, directory, fname):
        vmapper = {
            'time':         't',
            'bottom':       'bottom_iter',
            'mg':           'mg_iter',
            'linf':         'LINF',
            'l1':           'L1',
            'l2':           'L2'
        }
        
        lmapper  = {
            'linf':     r'max. $l_\infty$ residual error',
            'l1':       r'max. $l_1$ residual error',
            'l2':       r'max. $l_2$ residual error',
            'bottom':   r'#iterations of bottom solver',
            'mg':       r'#iterations of MG'
        }
        
        umapper = [
            'time'
        ]
        
        super(SolverDataset, self).__init__(directory, fname,
                                            variable_mapper=vmapper,
                                            label_mapper=lmapper,
                                            unit_label_mapper=umapper,
                                            dataset_type='Solver')
