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

from opal.parser.FieldParser import FieldParser
from opal.visualization.FieldPlotter import FieldPlotter
from .DatasetBase import DatasetBase
from opal.utilities.logger import opal_logger
import pandas as pd
import numpy as np
import os
import re

class FieldDataset(DatasetBase, FieldPlotter):
    """
    Attributes
    ----------
    _basename : str
        leading name all files have in common
    _directory : str
        the directory of all files
    _df  : pandas.core.frame.DataFrame
        the data of a single step (vector and scalar fields)
    _dim : list
        list of number of grid points per dimension
    _fields : dict
        the keys are the different fields and
        the values denotes 'scalar' or 'field'
    _loaded_step : int
        the number of the loaded file (if -1, no file
        is loaded)
    _npadding : int
        the number of digits in the number
        (used for zero padding)
    _parser : FieldParser
        class to parser field data
    _units : dict
    """

    def __init__(self, directory, fname):
        super(FieldDataset, self).__init__(directory, fname)

        self._parser = FieldParser()
        self._count_files(directory, fname)
        self._loaded_step = -1
        self._directory   = directory

        self._label_mapper = {
            'ex':   r'$E_x$',
            'ey':   r'$E_y$',
            'ez':   r'$E_z$',
            'phi':  r'$\phi$',
            'rho':  r'$\rho$'
        }

    def getData(self, var, step=0):
        self._load_step(step)
        return self._df[:, var].values

    def getLabel(self, var):
        if var in self._label_mapper:
            var = self._label_mapper[var]
        return var

    def getUnit(self, var):
        return self._units[var]

    @property
    def names(self):
        return list(self._df.keys())

    @property
    def dataframe(self):
        return self._df

    def getSlice(self, field, normal, pos=0.0, step=0, index=0):
        try:
            if normal == 'x':
                dim = 0
            elif normal == 'y':
                dim = 1
            elif normal == 'z':
                dim = 2
            else:
                raise ValueError("The normal can only be 'x', 'y' or 'z'.")

            dims = [0, 1, 2]
            del dims[dim]

            self._load_step(step)

            if index > 0:
                index = self._find_nearest(self.positions[:, dim], pos, dim)

            ## why do we need astype? Bug of pandas?
            nindex = self.indices[:, dim].astype(int)
            pos_1 = self.positions[nindex == index, dims[0]]
            pos_2 = self.positions[nindex == index, dims[1]]

            ff    = self._df[field].values[nindex == index]

            d = self._dim
            pos_1 = pos_1.reshape((d[dims[0]], d[dims[1]]))
            pos_2 = pos_2.reshape((d[dims[0]], d[dims[1]]))
            ff    = ff.reshape((d[dims[0]], d[dims[1]]))

            return pos_1, pos_2, ff
        except Exception as ex:
            opal_logger.exception(ex)
            return None

    def _find_nearest(self, array, value, dim):
        """Find nearest value is an array

        Reference: https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array (5. June 2020)
        """
        idx = (np.abs(array-value)).argmin()
        return int(self.indices[idx, dim])

    @property
    def indices(self):
        return self._df.values[:, 0:3]

    @property
    def positions(self):
        return self._df.values[:, 3:6]


    def __str__(self):
        if self._loaded_step == -1:
            self._load_step(0)
        s  = '\n\tField dataset.\n\n'
        s += '\tDimension:  ' + str(self._dim[0]) + ' x ' + \
            str(self._dim[1]) + ' x ' + str(self._dim[2]) + '\n\n'
        fields = list(self._df.keys())
        s += '\tAvailable fields (' + str(len(fields)) + ') :\n\n'
        for field in fields:
            s += '\t' + field + '\n'
        return s

    def _count_files(self, directory, fname):
        """
        Count the number of field files (scalar and vector fields).
        Store the names and the number of files in the
        dictionary self._fields.
        """

        pattern = r'(.*)-(.*)_(.*)-(\d+).dat'

        obj = re.match(pattern, fname)
        self._basename = obj.group(1)
        self._npadding = len(obj.group(4))

        scalar_pattern = r'' + self._basename + '-(.*)_scalar-(\d+).dat'
        field_pattern  = r'' + self._basename + '-(.*)_field-(\d+).dat'

        self._fields = {}
        count_scalar = 0
        count_field  = 0
        for fn in os.listdir(directory):
            obj = re.match(scalar_pattern, fn)
            if obj:
                count_scalar += 1
                if not obj.group(1) in self._fields.keys():
                    self._fields[obj.group(1)] = 'scalar'
                continue
            obj = re.match(field_pattern, fn)
            if obj:
                count_field += 1
                if not obj.group(1) in self._fields.keys():
                    self._fields[obj.group(1)] = 'field'

        print('Found', count_scalar, 'scalar field files.')
        print('Found', count_field, 'vector field files.')

    def _zero_padding(self, step):
        return str(step).zfill(self._npadding)

    def _get_combined_filename(self, step, field):
        """
        Parameters
        ----------
        step : int
            the time step
        field : str
            the field

        Returns
        -------
        str
            the full file name
        """
        # vector fields have 'x', 'y' and 'z' components
        return os.path.join(self._directory, self._basename + '-' + field + '_' + \
            self._fields[field] + '-' + self._zero_padding(step) + '.dat')

    def _load_step(self, step):
        """Load all fields of a single step. It merges
        the dataframes of the individual field files of
        a step.
        """
        if not self._loaded_step == step:
            self._df = pd.DataFrame()
            for f in self._fields.keys():
                self._parser.parse(self._get_combined_filename(step, f))
                df = self._parser.dataframe
                if not self._df.empty:
                    # 5. June 2020
                    # https://stackoverflow.com/questions/52913379/concat-dataframe-having-duplicate-columns/52913406
                    self._df =  self._df.merge(df, how='outer')
                    self._units.update(self._parser.get_unit_dictionary())
                else:
                    self._df = self._parser.dataframe
                    self._units = self._parser.get_unit_dictionary()
            self._loaded_step = step
            self._dim = self._parser.dimension
            # clear data in parser (not needed anymore)
            self._parser.clear()