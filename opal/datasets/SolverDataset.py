# Author:   Matthias Frey
# Date:     March 2018

import os
from opal.parser.SDDSParser import SDDSParser
from opal.datasets.DatasetBase import *
import numpy as np

class SolverDataset(DatasetBase):
    
    def __init__(self, directory, fname):
        """
        Constructor.
        
        Members
        -------
        __parser            (SDDSParser)    actual data holder
        __variable_mapper   (dict)          map user input variable
                                            name to file variable name
        __label_mapper      (dict)          map user input variable
                                            name to plot label name
        __unit_label_mapper ([])            map units of variables
                                            to plotting style
        """
        self.__parser = SDDSParser()
        
        self.__variable_mapper = {
            'time':         't',
            'bottom':       'bottom_iter',
            'mg':           'mg_iter',
            'linf':         'LINF',
            'l1':           'L1',
            'l2':           'L2'
        }
        
        self.__label_mapper  = {
            'linf':     r'max. $l_\infty$ residual error',
            'l1':       r'max. $l_1$ residual error',
            'l2':       r'max. $l_2$ residual error',
            'bottom':   r'#iterations of bottom solver',
            'mg':       r'#iterations of MG'
        }
        
        self.__unit_label_mapper = [
            'time'
        ]
        
        full_path = os.path.join(directory, fname)
        if not os.path.exists(full_path):
            raise RuntimeError("File '" + full_path + "' does not exist.")
        
        self.__parser.parse(full_path)
        
        super(SolverDataset, self).__init__(directory, fname)
    
    
    def getData(self, var, **kwargs):
        """
        Obtain the data of a variable
        
        Parameters
        ----------
        var     (str)   variable name
        
        Returns
        -------
        an array of the data
        """
        solvervar = var
        
        if var in self.__variable_mapper:
            solvervar = self.__variable_mapper[var]
        
        if not solvervar in self.__parser.getVariables():
            raise RuntimeError("The variable '" + var + "' is not in dataset.")
        return np.asarray(self.__parser.getDataOfVariable(solvervar))
    
    def getLabel(self, var):
        """
        Obtain label for plotting.
        
        Parameters
        ----------
        var     (str)   variable name
        
        Returns
        -------
        appropriate name plotting ready
        """
        solvervar = var
        
        if var in self.__variable_mapper:
            solvervar = self.__variable_mapper[var]
        
        if not solvervar in self.__parser.getVariables():
            raise RuntimeError("The variable '" + var + "' is not in dataset.")
        
        if var in self.__label_mapper:
            var = self.__label_mapper[var]
        
        return var
    
    
    def getUnit(self, var):
        """
        Obtain unit for plotting.
        
        Parameters
        ----------
        var     (str)   variable name
        
        Returns
        -------
        appropriate unit in math mode for plotting 
        """
        solvervar = var
        
        if var in self.__variable_mapper:
            solvervar = self.__variable_mapper[var]
        
        if not solvervar in self.__parser.getVariables():
            raise RuntimeError("The variable '" + var + "' is not in dataset.")
        
        unit = self.__parser.getUnitOfVariable(solvervar)
        
        if var in self.__unit_label_mapper:
            unit = r'\mathrm{' + unit + '}'
        
        return r'$' + unit + '$'


    @property
    def size(self):
        return self.__parser.size


    def __str__(self):
        variables = self.__parser.getVariables()
        s  = '\n\tSolver dataset.\n\n'
        s += '\tSize: ' + str(len(variables)) + ' x ' + str(self.size) + '\n\n'
        s += '\tAvailable variables (' + str(len(variables)) + ') :\n\n'
        for v in sorted(variables):
            s += '\t' + '%-20s' % (v) + '\t' + self.__parser.getDescriptionOfVariable(v) + '\n'
        return s
