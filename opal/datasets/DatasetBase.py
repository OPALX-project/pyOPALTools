# Author:   Matthias Frey
# Date:     March 2018

import os
from opal.datasets.filetype import FileType
from opal.utilities.logger import opal_logger

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
        try:
            full_path = os.path.join(directory, fname)
            if not os.path.exists(full_path):
                raise RuntimeError("File '" + full_path + "' does not exist.")
            
            self._directory = directory
            self._fname = fname
            self._ftype = FileType.extensionToFileType(os.path.join(directory, fname))
        except Exception as ex:
            opal_logger.exception(ex)
    
    
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
    
    @property
    def size(self):
        """
        To be implemented by derived class.
        """
        return None
    
    def __str__(self):
        """
        Print a short summary about the dataset.
        To be implemented in the derived classes.
        """
        return 'Empty dataset.'


    @property
    def ds(self):
        """
        Returns
        -------
        reference to dataset. Used in plotting classes.
        """
        return self
