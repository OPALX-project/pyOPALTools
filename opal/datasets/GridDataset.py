# Author:   Matthias Frey
# Date:     March 2018

import os
from opal.parser.SDDSParser import SDDSParser
from opal.datasets.DatasetBase import *
import numpy as np

class GridDataset(DatasetBase):
    
    def __init__(self, directory, fname):
        """
        Constructor.
        
        Members
        -------
        __parser            (SDDSParser)    actual data holder
        __variable_mapper   (dict)          map user input variable
                                            name to file variable name
        __unit_label_mapper ([])            map units of variables
                                            to plotting style
        """
        self.__parser = SDDSParser()
        
        self.__variable_mapper = {
            'time':         't'
        }
        
        self.__unit_label_mapper = [
            'time'
        ]
        
        full_path = os.path.join(directory, fname)
        if not os.path.exists(full_path):
            raise RuntimeError("File '" + full_path + "' does not exist.")
        
        self.__parser.parse(full_path)
        
        super(GridDataset, self).__init__(directory, fname)
    
    
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
        gridvar = var
        
        if var in self.__variable_mapper:
            gridvar = self.__variable_mapper[var]
        
        if not gridvar in self.__parser.getVariables():
            raise RuntimeError("The variable '" + var + "' is not in dataset.")
        return np.asarray(self.__parser.getDataOfVariable(gridvar))
    
    
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
        gridvar = var
        
        if var in self.__variable_mapper:
            gridvar = self.__variable_mapper[var]
        
        if not gridvar in self.__parser.getVariables():
            raise RuntimeError("The variable '" + var + "' is not in dataset.")
        
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
        gridvar = var
        
        if var in self.__variable_mapper:
            gridvar = self.__variable_mapper[var]
        
        if not gridvar in self.__parser.getVariables():
            raise RuntimeError("The variable '" + var + "' is not in dataset.")
        
        unit = self.__parser.getUnitOfVariable(gridvar)
        
        if var in self.__unit_label_mapper:
            unit = r'\mathrm{' + unit + '}'
        
        return r'$' + unit + '$'
    
    
    def getNumLevels(self):
        """
        Obtain the number of levels.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        an integer
        """
        variables = self.__parser.getVariables()
        return sum('level-' in var for var in variables)
    
    
    def getNumCores(self):
        """
        Obtain the number of cores.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        an integer
        """
        variables = self.__parser.getVariables()
        return sum('processor-' in var for var in variables)
