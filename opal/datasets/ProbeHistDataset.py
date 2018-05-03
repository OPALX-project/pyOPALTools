# Author:   Matthias Frey
# Date:     May 2018

import os
from utilities.HistogramParser import HistogramParser
from opal.datasets.DatasetBase import *
import numpy as np

class ProbeHistDataset(DatasetBase):
    
    def __init__(self, directory, fname):
        """
        Constructor.
        
        Members
        -------
        __parser            (HistogramParser)    actual data holder
        """
        self.__parser = HistogramParser()
        
        full_path = os.path.join(directory, fname)
        if not os.path.exists(full_path):
            raise RuntimeError("File '" + full_path + "' does not exist.")
        
        self.__parser.parse(full_path)
        
        super(ProbeHistDataset, self).__init__(directory, fname)
    
    
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
        if not self.__parser.isVariable(var):
            raise ValueError("The variable '" + var + "' is not in dataset.")
        return self.__parser.getDataOfVariable(var)
    
    
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
        if not self.__parser.isVariable(var):
            raise ValueError("The variable '" + var + "' is not in dataset.")
        
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
        if not self.__parser.isVariable(var):
            raise ValueError("The variable '" + var + "' is not in dataset.")
        
        unit = self.__parser.getUnitOfVariable(var)
        
        return r'$' + unit + '$'
