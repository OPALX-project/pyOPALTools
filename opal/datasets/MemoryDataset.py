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
from opal.visualization.MemoryPlotter import MemoryPlotter

class MemoryDataset(SDDSDatasetBase, MemoryPlotter):

    def __init__(self, directory, fname):
        """
        """
        vmapper = {
            'time':         't'
        }

        umapper = [
            'time'
        ]

        lmapper = {
            'VmHWM-Avg':    r'average VM HWM',
            'VmHWM-Max':    r'maximum VM HWM',
            'VmHWM-Min':    r'minimum VM HWM',
            'VmPeak-Avg':   r'average peak VM',
            'VmPeak-Max':   r'maximum peak VM',
            'VmPeak-Min':   r'minimum peak VM',
            'VmRSS-Avg':    r'average VM RSS',
            'VmRSS-Max':    r'maximum VM RSS',
            'VmRSS-Min':    r'minimum VM RSS',
            'VmSize-Avg':   r'average VM size',
            'VmSize-Max':   r'maximum VM size',
            'VmSize-Min':   r'minimum VM size',
            'VmStk-Avg':    r'average VM stack size',
            'VmStk-Max':    r'maximum VM stack size',
            'VmStk-Min':    r'minimum VM stack size'
        }

        super(MemoryDataset, self).__init__(directory, fname,
                                            variable_mapper=vmapper,
                                            label_mapper=lmapper,
                                            unit_label_mapper=umapper,
                                            dataset_type='Memory usage',
                                            print_limit=11)
