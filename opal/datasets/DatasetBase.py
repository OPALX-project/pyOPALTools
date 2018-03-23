# Author:   Matthias Frey
# Date:     March 2018

import os
from enum import IntEnum, unique

@unique
class FileType(IntEnum):
    H5     = 0,
    STAT   = 1,
    MEM    = 2,
    LBAL   = 3,
    OUTPUT = 4,
    TIMING = 5,
    GRID   = 6,
    SOLVER = 7,
    NONE   = 8,
    
    @classmethod
    def extensionToFileType(cls, fname):
        extension = {
            '.h5':      cls.H5,
            '.stat':    cls.STAT,
            '.mem':     cls.MEM,
            '.lbal':    cls.LBAL,
            '.out':     cls.OUTPUT,
            '.output':  cls.OUTPUT,
            '.grid':    cls.GRID,
            '.solver':  cls.SOLVER
        }
        
        file = {
            'timing.dat': cls.TIMING
        }
        
        _ , ext = os.path.splitext(fname)
        
        if ext in extension:
            return extension[ext]
        elif fname in file:
            return file[fname]
        elif 'time' in fname.lower() or 'timing' in fname.lower():
            # hopeful test for timing files
            return cls.TIMING
        else:
            return cls.NONE


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
    