# Author:   Matthias Frey
# Date:     March 2018

from timing.Timing import Timing
from opal.datasets.DatasetBase import *
import os

class TimeDataset(DatasetBase):
    
    def __init__(self, directory, fname, ttype='ippl'):
        """
        Constructor.
        
        Parameters
        ----------
        directory   (str)   of file
        fname       (str)   basename
        ttype       (str)   time file type ('ippl' timing or OPAL 'output')
        
        Members
        -------
        __parser            (Timing)    actual data holder
        """
        self.__parser = Timing()
        
        if ttype.lower() == 'output':
            self.__parser.read_output_file(os.path.join(directory, fname))
        elif ttype.lower() == 'ippl':
            self.__parser.read_ippl_timing(os.path.join(directory, fname))
        else:
            raise ValueError("Timing file type '" + ttpye + "' not supported." +
                             "Use either 'ippl' or 'output'")
        
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
