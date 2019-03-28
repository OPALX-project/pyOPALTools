# Author:   Matthias Frey
# Date:     May 2018

import os
from opal.parser.PeakParser import PeakParser
from opal.datasets.DatasetBase import DatasetBase
from opal.visualization.PeakPlotter import PeakPlotter
import numpy as np

class PeakDataset(DatasetBase, PeakPlotter):
    
    def __init__(self, directory, fname):
        """
        Constructor.
        
        Members
        -------
        __parser            (PeakParser)    actual data holder
        __variable_mapper   (dict)          map user input variable
        """
        self.__parser = PeakParser()
        
        self.__variable_mapper = {
            'radius':   'radii'
        }
        
        full_path = os.path.join(directory, fname)
        if not os.path.exists(full_path):
            raise RuntimeError("File '" + full_path + "' does not exist.")
        
        self.__parser.parse(full_path)
        
        super(PeakDataset, self).__init__(directory, fname)
    
    
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
        peakvar = var
        
        if var in self.__variable_mapper:
            peakvar = self.__variable_mapper[var]
        
        if not self.__parser.isVariable(peakvar):
            raise ValueError("The variable '" + var + "' is not in dataset.")
        
        return self.__parser.getDataOfVariable(peakvar)
    
    
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
        peakvar = var
        
        if var in self.__variable_mapper:
            peakvar = self.__variable_mapper[var]
        
        if not self.__parser.isVariable(peakvar):
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
        peakvar = var
        
        if var in self.__variable_mapper:
            peakvar = self.__variable_mapper[var]
        
        if not self.__parser.isVariable(peakvar):
            raise ValueError("The variable '" + var + "' is not in dataset.")
        
        unit = self.__parser.getUnitOfVariable(peakvar)
        
        return unit

    @property
    def size(self):
        return len(self.__parser.getDataOfVariable(self.__parser.getVariableName()[0]))


    def __str__(self):
        s  = '\n\tPeak dataset.\n\n'
        s += '\tSize: ' + str(self.size) + '\n\n'
        s += '\tType: ' + self.__parser.getType() + '\n'
        return s
