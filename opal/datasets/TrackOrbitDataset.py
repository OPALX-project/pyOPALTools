# Author:   Matthias Frey
# Date:     March 2018

import os
from utilities.TrackOrbitParser import TrackOrbitParser
from opal.datasets.DatasetBase import *
import numpy as np

class TrackOrbitDataset(DatasetBase):
    
    def __init__(self, directory, fname):
        """
        Constructor.
        
        Members
        -------
        __parser            (TrackOrbitParser)  actual data holder
        __unit_label_mapper ([])                map units of variables
                                                to plotting style
        """
        self.__parser = TrackOrbitParser()
        
        self.__unit_label_mapper = [
            'x',
            'y',
            'z'
        ]
        
        
        full_path = os.path.join(directory, fname)
        if not os.path.exists(full_path):
            raise RuntimeError("File '" + full_path + "' does not exist.")
        
        self.__parser.parse(full_path)
        
        super(TrackOrbitDataset, self).__init__(directory, fname)
    
    
    def getData(self, var, **kwargs):
        """
        Obtain the data of a variable
        
        Parameters
        ----------
        var     (str)   variable name
        
        Returns
        -------
        an array of the dataself
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
        if self.__parser.isVariable(var):
            return var
        else:
            raise RuntimeError("No variable '" + var + "' in dataset.")
    
    
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
            raise RuntimeError("No variable '" + var + "' in dataset.")
        
        unit = self.__parser.getUnitOfVariable(var)
        if var in self.__unit_label_mapper:
            unit = r'\mathrm{' + unit + '}'
        
        return r'$' + unit + '$'
