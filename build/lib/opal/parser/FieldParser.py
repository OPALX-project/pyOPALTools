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
import numpy as np
import collections
from .BaseParser import BaseParser

class FieldParser(BaseParser):
    """Read OPAL field data generated with compile flag DBG_SCALARFIELD enabled.

    Attributes
    ----------
    _columns: dict
        the keys are the column names and the values their units
    _df  : pandas.core.frame.DataFrame
        the data
    _dim : list
        list of number of grid points per dimension
    _stride : list
        list of stride per dimension
    """

    def __init__(self):
        """Constructor
        """
        self.clear()

    def parse(self, filename):
        """Parse a file.

        Parameters
        ----------
        filename : str
            the full name of a file to parse
        """
        if not self._check_header(filename):
            raise IOError("File '" + filename + "' is not a proper grid file.")

        col_types = self._parse_header(filename)

        self._df = pd.read_csv(filename, sep='\s+', comment='#', header=None,
                               names=list(col_types.keys()), dtype=col_types)

        for i in range(3):
            self._dim[i] = int(max(self.indices[:, i]) -
                               min(self.indices[:, i]) + 1)
            self._stride[i] = np.where(np.diff(self.indices[:, i]) == 1)[0][0] + 1

    @property
    def dataframe(self):
        """Get all data.

        Returns
        -------
        pandas.core.frame.DataFrame
            all the data
        """
        return self._df

    def clear(self):
        """Reset attributes
        """
        self._dim = [0, 0, 0]
        self._stride = [0, 0, 0]
        self._columns = {}
        self._df = None

    def get_unit_dictionary(self):
        """Get the dictionary of units.

        Returns
        -------
        dict :
            column names (keys) and their units (values)
        """
        return self._columns

    @property
    def field(self):
        """
        Returns
        -------
        numpy.ndarray
            the field data on the grid
        """
        # 'image' is the image potential of OPAL-T
        if 'image' in self._columns.keys():
            return self._df.values[:, 6]
        return self._df.values[:, 6:]

    @property
    def image(self):
        """
        Returns
        -------
        numpy.array
            the image potential (if available)
        """
        if 'image' in self._columns.keys():
            return self._df.values[:, 7]
        return None

    @property
    def indices(self):
        """
        Returns
        -------
        numpy.ndarray
            the grid point indices
        """
        return self._df.iloc[:, 0:3].values

    @property
    def positions(self):
        """
        Returns
        -------
        numpy.ndarray
            the positions at the grid points
        """
        return self._df.values[:, 3:6]

    @property
    def dimension(self):
        """
        Returns
        -------
        list
            the number of grid points per dimension
        """
        return self._dim


    @property
    def stride(self):
        """
        Returns
        -------
        list
            the stride per dimension
        """
        return self._stride


    def is_scalar(self):
        """
        Returns
        -------
        bool
            True if a scalar field
        """
        return self.field.shape[1] == 1

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
        col_types = collections.OrderedDict()

        # first entry is '#' --> skip
        for entry in header_line[1:]:
            if '[' in entry:
                self._columns[list(col_types.keys())[-1]] = entry.replace('[', '').replace(']', '')
            else:
                col_types[entry] = np.float64

        # add remaining columns that have no unit
        for entry in col_types.keys():
            if not entry in self._columns.keys():
                self._columns[entry] = ''
                col_types[entry] = np.int32
        return col_types