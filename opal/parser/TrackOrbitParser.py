# Copyright (c) 2018, Matthias Frey, Paul Scherrer Institut, Villigen PSI, Switzerland
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

import numpy as np

class TrackOrbitParser:

    def __init__(self):

        self._names = [ 'ID', 'x', 'px', 'y', 'py', 'z', 'pz' ]

        self._units = {
            self._names[0]:   '1',
            self._names[1]:   'm',
            self._names[2]:   r'\beta\gamma',
            self._names[3]:   'm',
            self._names[4]:   r'\beta\gamma',
            self._names[5]:   'm',
            self._names[6]:   r'\beta\gamma'
        }

        self._description = {
            self._names[0]:   'particle identity number',
            self._names[1]:   'particle coordinate in x',
            self._names[2]:   'particle momentum in x',
            self._names[3]:   'particle coordinate in y',
            self._names[4]:   'particle momentum in y',
            self._names[5]:   'particle coordinate in z',
            self._names[6]:   'particle momentum in z',
        }

        self._dataset = []


    def parse(self, filename):

        pattern =  '# Part. ID'
        match = False

        with open(filename) as f:
            for line in f:
                if '#' in line:
                    # 24. March
                    # https://stackoverflow.com/questions/2077897/substitute-multiple-whitespace-with-single-whitespace-in-python
                    line = ' '.join(line.split())
                    if pattern in line:
                        match = True
                else:
                    break

        if not match:
            raise RuntimeError('Not proper file format.')

        self._dataset = np.genfromtxt(filename,
                                      comments='#',
                                      delimiter = ' ',
                                      dtype=[(self._names[0], 'S3'), # change to 'unicode' for Python 3.6
                                             (self._names[1], np.float64),
                                             (self._names[2], np.float64),
                                             (self._names[3], np.float64),
                                             (self._names[4], np.float64),
                                             (self._names[5], np.float64),
                                             (self._names[6], np.float64)]
                                      )

        for i in range(len(self._dataset[self._names[0]])):
            self._dataset[self._names[0]][i] = self._dataset[self._names[0]][i][-1:]

    def getDataOfVariable(self, var):

        if var == self._names[0]:
            # 23. March
            # https://stackoverflow.com/questions/39371467/numpy-loadtxt-returns-string-repr-of-bytestring-instead-of-string
            return self._dataset[self._names[0]].astype('int')
        elif var in self._names:
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
    def description(self):
        return self._description

    @property
    def size(self):
        return len(self._dataset)
