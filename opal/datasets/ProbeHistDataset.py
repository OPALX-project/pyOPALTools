# Author:   Matthias Frey
# Date:     May 2018

import os
from opal.parser.HistogramParser import HistogramParser
from opal.datasets.DatasetBase import DatasetBase
from opal.visualization.ProbePlotter import ProbePlotter
import numpy as np

class ProbeHistDataset(DatasetBase, ProbePlotter):
    
    def __init__(self, directory, fname):
        """
        Constructor.
        
        Members
        -------
        __parser            (HistogramParser)    actual data holder
        __variable_mapper   (dict)          map user input variable
        __label_mapper      (dict)          map user input variable
        """
        self.__parser = HistogramParser()
        
        
        self.__variable_mapper = {
            #'bincount':     'dataset',
            'radius':       'radii'
        }
        
        self.__label_mapper  = {
            'bincount':     'bin count'
        }
        
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
        peakvar = var
        
        if var in self.__variable_mapper:
            peakvar = self.__variable_mapper[var]
        
        if not self.__parser.isVariable(peakvar):
            raise ValueError("The variable '" + var + "' is not in dataset.")
        
        unit = self.__parser.getUnitOfVariable(peakvar)
        
        return unit


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
