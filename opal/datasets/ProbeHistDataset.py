# Author:   Matthias Frey
# Date:     May 2018

import os
from opal.parser.HistogramParser import HistogramParser
from .DatasetBase import DatasetBase
from opal.visualization.ProbePlotter import ProbePlotter
import numpy as np
from opal.utilities.logger import opal_logger

class ProbeHistDataset(DatasetBase, ProbePlotter):
    """
    Attributes
    -------
    __parser : HistogramParser
        Actual data holder
    __variable_mapper : dict
        Map user input variable
    __label_mapper : dict
        Map user input variable
    """
    def __init__(self, directory, fname):
        """Constructor.
        """
        super(ProbeHistDataset, self).__init__(directory, fname)

        self.__parser = HistogramParser()
        self.__parser.parse(self.filename)

        self.__variable_mapper = {
            #'bincount':     'dataset',
            'radius':       'radii'
        }

        self.__label_mapper  = {
            'bincount':     'bin count'
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
            peakvar = var

            if var in self.__variable_mapper:
                peakvar = self.__variable_mapper[var]

            if not self.__parser.isVariable(peakvar):
                raise ValueError("The variable '" + var + "' is not in dataset.")

            if var in self.__label_mapper:
                var = self.__label_mapper[var]

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
        return self.__parser.size


    def __str__(self):
        variables = self.__parser.getVariables()
        s  = '\n\tProbe histogram dataset.\n\n'
        s += '\tSize: ' + str(self.size) + '\n\n'
        s += '\tAvailable variables (' + str(len(variables)) + ') :\n\n'
        for v in sorted(variables):
            s += '\t' + '%-20s' % (v) + '\n'
        return s
