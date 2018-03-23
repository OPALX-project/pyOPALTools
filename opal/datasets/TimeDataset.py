# Author:   Matthias Frey
# Date:     March 2018

from timing.Timing import Timing
from opal.datasets.DatasetBase import *

class TimeDataset(DatasetBase):
    
    def __init__(self, directory, fname):
        """
        Constructor.
        
        Members
        -------
        __parser            (Timing)    actual data holder
        """
        self.__parser = Timing()
        
        super(TimeDataset, self).__init__(directory, fname)
    
    
    def getData(self, var, **kwargs):
        """
        Obtain the timing data
        
        Parameters
        ----------
        var     (str)   variable name
        
        Returns
        -------
        the timing data
        """
        return self.__parser.getTiming()
    
    
    def getLabel(self, var):
        """
        Obtain label for plotting.
        
        Parameters
        ----------
        var     (str)   is returned
        
        Returns
        -------
        var
        """
        return var
    
    
    def getUnit(self, var):
        """
        Obtain unit for plotting.
        
        Parameters
        ----------
        var     (str)   unused
        
        Returns
        -------
        the string 's' for seconds
        """
        return r'$s$'
