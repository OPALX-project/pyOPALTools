# Copyright (c) 2020, Paul Scherrer Institut, Villigen PSI, Switzerland
# All rights reserved
#
# This file is part of pyOPALTools.
#
# pyOPALTools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# You should have received a copy of the GNU General Public License
# along with pyOPALTools. If not, see <https://www.gnu.org/licenses/>.

import numpy as np

class FieldParser:
    """Read OPAL field data generated with compile flag DBG_SCALARFIELD enabled.

    Attributes
    ----------
    _dim : list
        List of number of grid points per dimension
    _indices : numpy.ndarray
        Indices representing the grid points
    _field : numpy.ndarray
        Field on grid points
    """

    def __init__(self):
        self._dim = [0, 0, 0]

    def parse(self, filename):
        data = np.loadtxt(filename, unpack=False, skiprows=0)

        self._indices = data[:, 0:3]
        self._field = data[:, 3:]

        for i in range(3):
            self._dim[i] = int(max(self._indices[:, i]) -
                               min(self._indices[:, i]) + 1)

        ni = self._dim[0]
        nj = self._dim[1]
        nk = self._dim[2]

        self._field = self._field.reshape((ni, nj, nk, self._field.shape[1]))
        self._indices = self._indices.reshape((ni, nj, nk, 3))

    @property
    def field(self):
        return self._field

    @property
    def indices(self):
        return self._indices

    @property
    def dimension(self):
        return self._dim

    def shape(self):
        return self._field.shape

    def is_scalar(self):
        return self._field.shape[3] == 1
