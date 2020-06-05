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
from .DatasetBase import DatasetBase
from opal.utilities.logger import opal_logger
import numpy as np

class FieldDataset(DatasetBase):

    def __init__(self, directory, fname):
        super(FieldDataset, self).__init__(directory, fname)

        self._parser = FieldParser()
        self._parser.parse(self.filename)

    def getData(self, step=0):
        return self._parser.field

    def getSlice(self, normal, index = 0):
        try:
            if normal == 'x':
                dim = 0
            elif normal == 'y':
                dim = 1
            elif normal == 'z':
                dim = 2
            else:
                raise ValueError("The normal can only by 'x', 'y' or 'z'.")

            d = self._parser.dimension
            if index < 0 or index > d[dim] - 1:
                raise IndexError("Bad grid point '" + str(index) + "'.")

            if dim == 0:
                return self._parser.positions[index,:,:, 1:3], self._parser.field[index,:,:]
            elif dim == 1:
                return self._parser.positions[:, index, :][:,:, [0, 2]], self._parser.field[:,index,:]
            elif dim == 2:
                return self._parser.positions[:,:,index, 0:2], self._parser.field[:,:,index]
            else:
                raise IndexError("Bad dimension '" + str(dim) + "'.")
        except Exception as ex:
            opal_logger.exception(ex)
            return None


        self._parser.field

    def __str__(self):
        s  = '\n\tField dataset.\n\n'

        field_type = 'vector'
        if self._parser.is_scalar():
            field_type = 'scalar'

        s += '\tType:       ' + field_type + ' field \n\n'
        dim = self._parser.dimension
        s += '\tDimension:  ' + str(dim[0]) + ' x ' + \
            str(dim[1]) + ' x ' + str(dim[2]) + '\n\n'
        return s
