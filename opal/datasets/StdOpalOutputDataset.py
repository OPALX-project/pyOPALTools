# Author:   Matthias Frey
# Date:     April 2018

from .DatasetBase import DatasetBase
from opal.visualization.StdOpalOutputPlotter import StdOpalOutputPlotter
from opal.analysis.StdOpalOutputAnalysis import StdOpalOutputAnalysis
import numpy as np

class StdOpalOutputDataset(DatasetBase, StdOpalOutputPlotter, StdOpalOutputAnalysis):
    
    def __init__(self, directory, fname):
        """
        Constructor.
        
        Members
        ----------
        None
        """
        super(StdOpalOutputDataset, self).__init__(directory, fname)
    
    def getData(self, var, **kwargs):
        """
        Obtain filename
        
        Parameters
        ----------
        var     (str)   unused
        
        Returns
        -------
        filename
        """
        return self.filename
    
    
    def getLabel(self, var):
        """
        Obtain label for plotting.
        
        Parameters
        ----------
        var     (str)   unused
        
        Returns
        -------
        empty string
        """
        return ''
    
    
    def getUnit(self, var):
        """
        Obtain unit for plotting.
        
        Parameters
        ----------
        var     (str)   unused
        
        Returns
        -------
        empty string
        """
        return ''
    
    @property
    def size(self):
        return 0
