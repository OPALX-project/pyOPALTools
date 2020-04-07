# Author:   Matthias Frey
# Date:     April 2019

import os
from opal.parser.LossParser import LossParser
from .DatasetBase import DatasetBase
import numpy as np
from opal.utilities.logger import opal_logger

class LossDataset(DatasetBase):
    """
    Attributes
    ----------
    __parser : LossParser
        Actual data holder
    __unit_label_mapper : list
        Units of variables
        to plotting style
    """
    def __init__(self, directory, fname):
        """Constructor.
        """
        super(LossDataset, self).__init__(directory, fname)

        self.__parser = LossParser()
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
            an array of the data
        """
        return np.asarray(self.__parser.getDataOfVariable(var))


    def getLabel(self, var):
        """Obtain label for plotting.

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
        s  = '\n\tLoss dataset.\n\n'
        variables = self.__parser.getVariableNames()
        s += '\tSize: ' + str(len(variables)) + ' x ' + str(self.size) + '\n\n'
        s += '\tAvailable variables (' + str(len(variables)) + ') :\n\n'
        for v in sorted(variables):
            s += '\t' + '%-20s' % (v) + \
                 '\t' + self.__parser.getUnitOfVariable(v) + '\n'
        return s
