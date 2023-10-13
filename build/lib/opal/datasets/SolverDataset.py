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
from opal.visualization.SolverPlotter import SolverPlotter

class SolverDataset(SDDSDatasetBase, SolverPlotter):

    def __init__(self, directory, fname):
        """
        """
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
