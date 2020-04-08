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

from .DatasetBase import DatasetBase
from opal.visualization.AmrPlotter import AmrPlotter
from opal.utilities.logger import opal_logger

class AmrDataset(DatasetBase, AmrPlotter):
    """Dataset of AMR output. It uses (https://yt-project.org/) to parse the data.
    An OPAL-AMR fork is found in https://gitlab.psi.ch/frey_m/yt.
    """

    def __init__(self, directory):
        """

        Parameters
        ----------
        directory : list
            Directory name that contains a Header file and Level_x
            (x = 0, 1, 2, ...) directories.
        """
        import yt

        self._ds = yt.load(directory, dataset_type='boxlib_opal')

        super(AmrDataset, self).__init__(directory, 'Header')


    @property
    def real_ds(self):
        return self._ds


    def get_ray_along(self, axis, field, **kwargs):
        """

        Parameters
        ----------
        axis : str
            Take a line cut along this axis ('x', 'y', 'z')
        field : str
            y-axis parameter
        center : (float, float), optional
            Center through which line should go

        Returns
        -------
        array
        array
        tuple
            center

        Notes
        -----
        27. May 2018
        http://yt-project.org/doc/visualizing/manual_plotting.html
        """
        import numpy as np

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

        center = kwargs.pop('center', (None, None))

        if center == (None, None):
            c = self.ds.real_ds.find_max(field)[1]
            center = (c[cut1], c[cut2])

        ray = self.ds.real_ds.ortho_ray(ax, center)

        srt = np.argsort(ray[axis])

        return np.array(ray[axis][srt]), np.array(ray[field][srt]), center


    def __str__(self):
        s  = '\n\tAMR dataset.\n\n'
        s += '\tAvailable fields (' + str(len(self._ds.field_list)) + ') :\n\n'
        for field in self._ds.field_list:
            s += '\t    ' + field[1] + '\n'
        s += '\n\tAvailable derived fields (' + str(len(self._ds.derived_field_list)) + ') :\n\n'
        for dfield in self._ds.derived_field_list:
            s += '\t    ' + dfield[1] + '\n'
        return s
