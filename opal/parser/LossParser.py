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

import re
import numpy as np
from .BaseParser import BaseParser

class LossParser(BaseParser):

    def __init__(self):
        self.clear()

    def parse(self, filename):
        """Parser method for loss files

        Examples
        --------

        **1. Clean**

        line = "# Element STQ1 x (mm),  y (mm),  z (mm),  px ( ),  py ( ),  pz ( ), id,  turn,  time (ns)"

        gets

        line = " x (mm),  y (mm),  z (mm),  px ( ),  py ( ),  pz ( ), id,  turn,  time (ns)"

        **2. no commas**

        line = " x (mm),  y (mm),  z (mm),  px ( ),  py ( ),  pz ( ), id,  turn,  time (ns)"

        gets

        line = " x (mm)   y (mm)   z (mm)   px ( )   py ( )   pz ( )  id   turn   time (ns)"
        """
        line = ''

        # 4. April 2019
        # https://stackoverflow.com/questions/1904394/read-only-the-first-line-of-a-file
        with open(filename) as f:
            line = f.readline()

        # 1. step
        line = re.sub(r"# Element (\S+)", ' ', line)

        # 2. step
        line = re.sub(r',', ' ', line)

        # 3. step
        pattern = '(\\w+) (\\(\\w+\\))?'

        quantities = re.findall(pattern, line)

        dtypes = [ ('element', str) ] # change to 'unicode' for Python 3.6


        for quan in quantities:
            self._names.append( quan[0] )
            unit = quan[1].replace(')', '')
            unit = unit.replace('(', '')
            self._units[quan[0]] = unit

            dtypes.append( (quan[0], float) )

        self._dataset = np.genfromtxt(filename,
                                      comments='#',
                                      dtype=dtypes)

    def clear(self):
        """Clear data.
        """
        self._names = [ 'element' ]

        self._units = { 'element': '' }

        self._dataset = []


    def getDataOfVariable(self, var):
        if var in self._names:
            return self._dataset[var]
        else:
            raise RuntimeError("No variable '" + var + "' in dataset.")


    def getUnitOfVariable(self, var):
        if var in self._names:
            return self._units[var]
        else:
            raise RuntimeError("No variable '" + var + "' in dataset.")


    def isVariable(self, var):
        return var in self._names


    def getVariableNames(self):
        return self._names

    @property
    def size(self):
        return len(self._dataset)
