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

import pandas as pd

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
    _columns: dict
        The keys are the column names and the values their units.
    """

    def __init__(self):
        self._dim = [0, 0, 0]
        self._columns =  {}

    def parse(self, filename):
        if not self._check_header(filename):
            raise IOError("File '" + filename + "' is not a proper grid file.")

        self._parse_header(filename)

        df = pd.read_csv(filename, sep='\s+', comment='#', header=None)

        self._indices   = df.values[:, 0:3]
        self._positions = df.values[:, 3:6]
        self._field     = df.values[:, 6:]

        for i in range(3):
            self._dim[i] = int(max(self._indices[:, i]) -
                               min(self._indices[:, i]) + 1)

        ni = self._dim[0]
        nj = self._dim[1]
        nk = self._dim[2]

        self._field     = self._field.reshape((ni, nj, nk, self._field.shape[1]))
        self._indices   = self._indices.reshape((ni, nj, nk, 3))
        self._positions = self._positions.reshape((ni, nj, nk, 3))

    @property
    def field(self):
        """
        Returns
        -------
        numpy.ndarray
            The field data on the grid.
        """
        return self._field

    @property
    def indices(self):
        """
        Returns
        -------
        numpy.ndarray
            The grid point indices.
        """
        return self._indices

    @property
    def dimension(self):
        """
        Returns
        -------
        list
            The number of grid points per dimension.
        """
        return self._dim


    def is_scalar(self):
        """Check if a scalar field
        """
        return self._field.shape[3] == 1

    def _check_header(self, filename):
        # check the first line
        with open(filename) as f:
            line = f.readline()
        if 'data on grid' in line:
            return True
        return False

    def _parse_header(self, filename):
        # clear
        self._columns = {}

        # the last comment line contains the quantities
        with open(filename) as ff:
            for i, line in enumerate(ff):
                if '#' in line:
                    header_line = line
                else:
                    break

        header_line = header_line.split()
        col = ''
        # first entry is '#' --> skip
        for entry in header_line[1:]:
            if '[' in entry:
                self._columns[col] = entry.replace('[', '').replace(']', '')
            else:
                col = entry

        # add remaining columns that have no unit
        for entry in header_line[1:]:
            if not entry in self._columns.keys() and not '[' in entry:
                self._columns[entry] = None

    def check_file(self, filename):
        """Check if a field file.

        Parameters
        ----------
        filename : str
           file to be checked
        """
        try:
            self.parse(filename)
        except:
            return False
        return True
