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

import os
from opal.parser.TrackOrbitParser import TrackOrbitParser
from .DatasetBase import DatasetBase
from opal.visualization.TrackOrbitPlotter import TrackOrbitPlotter
from opal.analysis.TrackOrbitAnalysis import TrackOrbitAnalysis
import numpy as np
from opal.utilities.logger import opal_logger

class TrackOrbitDataset(DatasetBase, TrackOrbitPlotter, TrackOrbitAnalysis):
    """
    Attributes
    ----------
    __parser : TrackOrbitParser
        Actual data holder
    __unit_label_mapper : list
        Units of variables
        to plotting style
    """
    def __init__(self, directory, fname):
        """Constructor.
        """
        super(TrackOrbitDataset, self).__init__(directory, fname)

        self.__parser = TrackOrbitParser()
        self.__parser.parse(self.filename)

        self.__unit_label_mapper = [
            'x',
            'y',
            'z'
        ]


    def getData(self, var, **kwargs):
        """Obtain the data of a variable

        Parameters
        ----------
        var : str
            Variable name

        Returns
        -------
        array
            Array of the data
        """
        return np.asarray(self.__parser.getDataOfVariable(var))

    def getLabel(self, var):
        """
        Obtain label for plotting.

        Parameters
        ----------
        var : str
            Variable name

        Returns
        -------
        str
            Appropriate name plotting ready
        """
        try:
            if self.__parser.isVariable(var):
                return var
            else:
                raise RuntimeError("No variable '" + var + "' in dataset.")
        except Exception as ex:
            opal_logger.exception(ex)
            return ''


    def getUnit(self, var):
        """Obtain unit for plotting.

        Parameters
        ----------
        var : str
            Variable name

        Returns
        -------
        str
            Appropriate unit in math mode for plotting
        """
        try:
            if not self.__parser.isVariable(var):
                raise RuntimeError("No variable '" + var + "' in dataset.")

            unit = self.__parser.getUnitOfVariable(var)
            if var in self.__unit_label_mapper:
                unit = r'\mathrm{' + unit + '}'

            return r'$' + unit + '$'
        except Exception as ex:
            opal_logger.exception(ex)
            return ''


    @property
    def size(self):
        return self.__parser.size


    def __str__(self):
        s  = '\n\tTrack Orbit dataset.\n\n'
        variables = self.__parser.getVariableNames()
        s += '\tSize: ' + str(len(variables)) + ' x ' + str(self.size) + '\n\n'
        s += '\tAvailable variables (' + str(len(variables)) + ') :\n\n'
        for v in sorted(variables):
            s += '\t' + '%-20s' % (v) + '\t' + '%-25s' % (self.__parser.description[v]) + \
                 '\t' + self.__parser.getUnitOfVariable(v) + '\n'
        return s
