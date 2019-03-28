# Author:   Matthias Frey
# Date:     April 2018

from opal.datasets.DatasetBase import DatasetBase
from opal.visualization.OutputPlotter import OutputPlotter
import numpy as np

class OutputDataset(DatasetBase, OutputPlotter):
    
    def __init__(self, directory, fname):
        """
        Constructor.
        
        Members
        ----------
        None
        """
        
        full_path = os.path.join(directory, fname)
        if not os.path.exists(full_path):
            raise RuntimeError("File '" + full_path + "' does not exist.")
        
        super(OutputDataset, self).__init__(directory, fname)
    
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
