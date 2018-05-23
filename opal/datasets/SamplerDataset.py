# Author:   Matthias Frey
# Date:     May 2018

import os
from opal.parser.sampler import SamplerParser
from opal.datasets.DatasetBase import *
from string import digits

class SamplerDataset(DatasetBase):
    
    def __init__(self, directory, fname):
        """
        Constructor.
        
        Parameters
        ----------
        directory           (str)                   directory name
        fname               (str)                   generation file name
        
        Members
        -------
        __parser            (SamplerParser)         actual data holder
        """
        
        full_path = os.path.join(directory, fname)
        if not os.path.exists(full_path):
            raise ValueError("File '" + full_path + "' does not exist.")
        
        self.__parser = SamplerParser()
        
        super(SamplerDataset, self).__init__(directory, fname)
    
    
    def getData(self, var, **kwargs):
        """
        Obtain the input data of a design variable
        of an individual. In order to select a specific
        individual set parameter 'ind' >= 0. If 'ind'
        is not given, the function takes the default value 0.
        
        Parameters
        ----------
        var     (str)   a design variable
        
        Optionals
        ---------
        ind     (int)   individual identity number
        
        Returns
        -------
        design variable simulation input value.
        """
        ind = kwargs.get('ind', 0)
        
        if not ind == -1:
            return self.__parser.getIndividualWithID(ind)
        
        if not var in self.__parser.design_variables:
            raise ValueError("The variable '" + var + "' is not in dataset.")
        
        return self.__parser.getIndividual(ind)
    
    
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
        if not var in self.__parser.design_variables:
            raise ValueError("The variable '" + var + "' is not in dataset.")
        
        return var
    
    
    def getUnit(self, var):
        """
        Obtain unit for plotting.
        
        Note: The optimizer does not yet write the units
              of each variable to the files. This function
              raises an error.
        
        Parameters
        ----------
        var     (str)   variable name
        
        Returns
        -------
        None
        """
        
        #FIXME
        raise RuntimeError("The sampler does not yet provide units.")
        
        return
    
    
    @property
    def design_variables(self):
        """
        Obtain design variable names
        """
        return self.__parser.design_variables
    
    
    @property
    def bounds(self):
        """
        Obtain design variable upper and lower bounds
        """
        return self.__parser.bounds
