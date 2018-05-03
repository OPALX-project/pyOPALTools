# Author:   Matthias Frey
# Date:     March 2018

import os
from opal.datasets.filetype import FileType

class DatasetBase:
    """
    Class with member functions common to
    all datasets.
    """
    
    def __init__(self, directory, fname):
        """
        Constructor.
        
        Members
        ----------
        _directory  (str)           of file
        _fname      (str)           name of file
        _ftype      (FileType)      type of file
        """
        self._directory = directory
        self._fname = fname
        self._ftype = FileType.extensionToFileType(fname)
        
    @property
    def filetype(self):
        return self._ftype
    
    @property
    def filename(self):
        return os.path.join(self._directory, self._fname)
    
    
    def getData(var, **kwargs):
        """
        To be implemented by derived class.
        """
        pass
    
    
    def getUnit(var):
        """
        To be implemented by derived class.
        """
        pass
    
    
    def getLabel(var):
        """
        To be implemented by derived class.
        """
        pass
    