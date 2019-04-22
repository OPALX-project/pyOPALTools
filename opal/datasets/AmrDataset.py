# Author: Matthias Frey
# Date:   March 2019

from .DatasetBase import DatasetBase
from opal.visualization.AmrPlotter import AmrPlotter
from opal.utilities.logger import opal_logger

class AmrDataset(DatasetBase, AmrPlotter):
    
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

    
    def get_ray_along(self, axis, field):
        """
        Parameters
        ----------
        axis    (str)           take a line cut along this axis
                                ('x', 'y', 'z')
        field   (str)
        
        Returns
        -------
        two rays
        """
        import numpy as np
        
        # 27. May 2018
        # http://yt-project.org/doc/visualizing/manual_plotting.html
        cut1 = 1
        cut2 = 2
        
        ax = 0
        if axis == 'y':
            ax = 1
            cut1 = 0
            cut2 = 2
        elif axis == 'z':
            ax = 2
            cut1 = 0
            cut2 = 1
        elif not axis == 'x':
            opal_logger.error("AmrDataset: Use either 'x', 'y' or 'z' axis")
        
        c = self.ds.real_ds.find_max(field)[1]
        ray = self.ds.real_ds.ortho_ray(ax, (c[cut1], c[cut2]))
        
        srt = np.argsort(ray[axis])
        
        return np.array(ray[axis][srt]), np.array(ray[field][srt])


    def __str__(self):
        s  = '\n\tAMR dataset.\n\n'
        s += '\tAvailable fields (' + str(len(self._ds.field_list)) + ') :\n\n'
        for field in self._ds.field_list:
            s += '\t    ' + field[1] + '\n'
        s += '\n\tAvailable derived fields (' + str(len(self._ds.derived_field_list)) + ') :\n\n'
        for dfield in self._ds.derived_field_list:
            s += '\t    ' + dfield[1] + '\n'
        return s
