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

import os
from opal.parser.SDDSParser import SDDSParser
from .DatasetBase import DatasetBase
import numpy as np
from opal.utilities.logger import opal_logger

class SDDSDatasetBase(DatasetBase):
    """
    Attributes
    ----------
    _parser : SDDSParser
        Actual data holder
    _variable_mapper : dict
        Map user input variable
        name to file variable name
    _label_mapper : dict
        Map user input variable
        name to plot label name
    _unit_label_mapper : list
        Units of variables
        to plotting style
    """
    def __init__(self, directory, fname, **kwargs):
        """Constructor.
        """
        super(SDDSDatasetBase, self).__init__(directory, fname)

        self._parser = SDDSParser()
        self._parser.parse(self.filename)

        self._variable_mapper = kwargs.pop('variable_mapper', {})

        self._label_mapper  = kwargs.pop('label_mapper', {})

        self._unit_label_mapper = kwargs.pop('unit_label_mapper', [])

        self._dataset_type = kwargs.pop('dataset_type', 'No')

        self._print_limit = kwargs.pop('print_limit', -1)


    def getData(self, var, **kwargs):
        """Obtain data of a variable

        Parameters
        ----------
        var : str
            Variable name

        Returns
        -------
        list
            List of the data
        """
        try:
            sddsvar = var

            if var in self._variable_mapper:
                sddsvar = self._variable_mapper[var]

            if not sddsvar in self._parser.getVariables():
                raise RuntimeError("The variable '" + var + "' is not in dataset.")
            return np.asarray(self._parser.getDataOfVariable(sddsvar))
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
            Appropriate name plotting ready
        """
        try:
            sddsvar = var

            if var in self._variable_mapper:
                sddsvar = self._variable_mapper[var]

            if not sddsvar in self._parser.getVariables():
                raise RuntimeError("The variable '" + var + "' is not in dataset.")

            if var in self._label_mapper:
                var = self._label_mapper[var]

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
            sddsvar = var

            if var in self._variable_mapper:
                sddsvar = self._variable_mapper[var]

            if not sddsvar in self._parser.getVariables():
                raise RuntimeError("The variable '" + var + "' is not in dataset.")

            unit = self._parser.getUnitOfVariable(sddsvar)

            if var in self._unit_label_mapper:
                unit = r'\mathrm{' + unit + '}'

            return r'$' + unit + '$'
        except Exception as ex:
            opal_logger.exception(ex)
            return ''


    def getVariables(self):
        """Obtain all variables within file.

        Returns
        -------
        list
            List of strings
        """
        return self._parser.getVariables()


    @property
    def size(self):
        return self._parser.size


    @property
    def dataframe(self):
        return self._parser.dataframe


    def getRow(self, var, val):
        """Obtain a row of a dataset

        Parameters
        ----------
        var : str
            Variable name
        val : float
            Value of given variable
        """
        try:
            sddsvar = var

            if var in self._variable_mapper:
                sddsvar = self._variable_mapper[var]

            if not sddsvar in self._parser.getVariables():
                raise RuntimeError("The variable '" + var + "' is not in dataset.")

            df = self._parser.dataframe
            if isinstance(val, str):
                return df[df[sddsvar] == val]
            else:
                # 31. August 2019
                # https://stackoverflow.com/questions/52587436/find-row-closest-value-to-input
                idx = df[sddsvar].sub(val).abs().idxmin()
                return df.loc[[idx]]

        except Exception as ex:
            opal_logger.exception(ex)
            return []


    def __str__(self):
        variables = sorted(self._parser.getVariables())
        nvar = len(variables)
        s  = '\n\t' + self._dataset_type + ' dataset.\n\n'
        s += '\tSize: ' + str(nvar) + ' x ' + str(self.size) + '\n\n'
        s += '\tAvailable variables (' + str(nvar) + ') :\n\n'
        if self._print_limit < nvar:
            for v in variables:
                s += '\t' + '%-20s' % (v) + '\t' + self._parser.getDescriptionOfVariable(v) + '\n'
        else:
            s += '\t' + '%-20s' % (variables[0]) + '\t' + self._parser.getDescriptionOfVariable(variables[0]) + '\n'
            s += '\t' + '%-20s' % (variables[1]) + '\t' + self._parser.getDescriptionOfVariable(variables[1]) + '\n'
            s += '\t' + '%-20s' % (variables[2]) + '\t' + self._parser.getDescriptionOfVariable(variables[2]) + '\n'
            s += '\t...\n'
            s += '\t' + '%-20s' % (variables[-2]) + '\t' + self._parser.getDescriptionOfVariable(variables[-2]) + '\n'
            s += '\t' + '%-20s' % (variables[-1]) + '\t' + self._parser.getDescriptionOfVariable(variables[-1]) + '\n'
        return s
