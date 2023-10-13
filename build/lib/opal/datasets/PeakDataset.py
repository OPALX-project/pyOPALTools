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
from opal.parser.PeakParser import PeakParser
from .DatasetBase import DatasetBase
from opal.visualization.PeakPlotter import PeakPlotter
import numpy as np
from opal.utilities.logger import opal_logger

class PeakDataset(DatasetBase, PeakPlotter):
    """
    Attributes
    ----------
    __parser : PeakParser
        Actual data holder
    __variable_mapper : dict
        Map user input variable
    """
    def __init__(self, directory, fname):
        """Constructor.
        """
        super(PeakDataset, self).__init__(directory, fname)

        self.__parser = PeakParser()
        self.__parser.parse(self.filename)

        self.__variable_mapper = {
            'radius':   'radii'
        }


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
        try:
            peakvar = var

            if var in self.__variable_mapper:
                peakvar = self.__variable_mapper[var]

            if not self.__parser.isVariable(peakvar):
                raise ValueError("The variable '" + var + "' is not in dataset.")

            return self.__parser.getDataOfVariable(peakvar)
        except Exception as ex:
            opal_logger.exception(ex)
            return []


    def getLabel(self, var):
        """Obtain label for plotting.

        Parameters
        ----------
        var : str
            Variable name

        Returns
        -------
        str
            appropriate name plotting ready
        """
        try:
            peakvar = var

            if var in self.__variable_mapper:
                peakvar = self.__variable_mapper[var]

            if not self.__parser.isVariable(peakvar):
                raise ValueError("The variable '" + var + "' is not in dataset.")

            return var
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
            peakvar = var

            if var in self.__variable_mapper:
                peakvar = self.__variable_mapper[var]

            if not self.__parser.isVariable(peakvar):
                raise ValueError("The variable '" + var + "' is not in dataset.")

            unit = self.__parser.getUnitOfVariable(peakvar)

            return unit
        except Exception as ex:
            opal_logger.exception(ex)
            return ''

    @property
    def size(self):
        return len(self.__parser.getDataOfVariable(self.__parser.getVariableName()[0]))


    def __str__(self):
        s  = '\n\tPeak dataset.\n\n'
        s += '\tSize: ' + str(self.size) + '\n\n'
        s += '\tType: ' + self.__parser.getType() + '\n'
        return s
