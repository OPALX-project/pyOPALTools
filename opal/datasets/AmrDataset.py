# Author: Matthias Frey
# Date:   March 2019

from opal.datasets.DatasetBase import *
from opal.utilities.logger import opal_logger

class AmrDataset(DatasetBase):
    
    def __init__(self, directory):
        """
        directory (list)  directory name that contains a Header file and Level_x
                          (x = 0, 1, 2, ...) directories.
        showme  (str)     print fields and derived fields in dataset
        """
        import yt
        
        self._ds = yt.load(directory, dataset_type='boxlib_opal')
        
        super(AmrDataset, self).__init__(directory, 'Header')
    
    
    @property
    def real_ds(self):
        return self._ds
    
    def __str__(self):
        s  = '\n\tAMR dataset.\n\n'
        s += '\tAvailable fields (' + str(len(self._ds.field_list)) + ') :\n\n'
        for field in self._ds.field_list:
            s += '\t    ' + field[1] + '\n'
        s += '\n\tAvailable derived fields (' + str(len(self._ds.derived_field_list)) + ') :\n\n'
        for dfield in self._ds.derived_field_list:
            s += '\t    ' + dfield[1] + '\n'
        return s
