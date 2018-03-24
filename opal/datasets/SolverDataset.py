# Author:   Matthias Frey
# Date:     March 2018

import os
from utilities.SDDSParser import SDDSParser
from opal.datasets.DatasetBase import *
import numpy as np

class SolverDataset(DatasetBase):
    
    def __init__(self, directory, fname):
        """
        Constructor.
        
        Members
        -------
        __parser        (SDDSParser)     actual data holder
        """
        self.__parser = SDDSParser()
        
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
        return np.asarray(self.__parser.getDataOfVariable(var))
    
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
        return r'$' + self.__parser.getUnitOfVariable(var) + '$'
