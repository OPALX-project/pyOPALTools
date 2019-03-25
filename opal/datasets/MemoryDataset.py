# Author:   Matthias Frey
# Date:     March 2018

import os
from opal.parser.SDDSParser import SDDSParser
from opal.datasets.DatasetBase import *
import numpy as np

class MemoryDataset(DatasetBase):
    
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
        
        super(MemoryDataset, self).__init__(directory, fname)
    
    
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
        return r'$\mathrm{' + self.__parser.getUnitOfVariable(var) + '}$'
    
    
    def getVariables(self):
        """
        Obtain all variables within file.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        list of strings
        """
        return self.__parser.getVariables()


    @property
    def size(self):
        return self.__parser.size

    def __str__(self):
        variables = self.__parser.getVariables()
        n = len(variables)
        s  = '\n\tLoad balancing dataset.\n\n'
        s += '\tSize: ' + str(n) + ' x ' + str(self.size) + '\n\n'
        s += '\tAvailable variables (' + str(n) + ') :\n\n'
        vv = sorted(variables)
        if n < 11:
            for v in vv:
                s += '\t' + '%-20s' % (v) + '\t' + self.__parser.getDescriptionOfVariable(v) + '\n'
        else:
            s += '\t' + '%-20s' % (vv[0]) + '\t' + self.__parser.getDescriptionOfVariable(vv[0]) + '\n'
            s += '\t' + '%-20s' % (vv[1]) + '\t' + self.__parser.getDescriptionOfVariable(vv[1]) + '\n'
            s += '\t' + '%-20s' % (vv[2]) + '\t' + self.__parser.getDescriptionOfVariable(vv[2]) + '\n'
            s += '\t...\n'
            s += '\t' + '%-20s' % (vv[-2]) + '\t' + self.__parser.getDescriptionOfVariable(vv[-2]) + '\n'
            s += '\t' + '%-20s' % (vv[-1]) + '\t' + self.__parser.getDescriptionOfVariable(vv[-1]) + '\n'
            
        return s
