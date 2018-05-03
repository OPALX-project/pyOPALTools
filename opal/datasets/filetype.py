# Author:   Matthias Frey
# Date:     March 2018

import os
from enum import IntEnum, unique

@unique
class FileType(IntEnum):
    H5          = 0,
    STAT        = 1,
    MEM         = 2,
    LBAL        = 3,
    OUTPUT      = 4,
    TIMING      = 5,
    GRID        = 6,
    SOLVER      = 7,
    TRACK_ORBIT = 8,
    PEAK        = 9,
    HIST        = 10,
    NONE        = 11
    
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
            '.solver':  cls.SOLVER,
            '.peaks':   cls.PEAK,
            '.hist':    cls.HIST
        }
        
        file = {
            'timing.dat':       cls.TIMING,
            '-trackOrbit.dat':  cls.TRACK_ORBIT
        }
        
        _ , ext = os.path.splitext(fname)
        
        if ext in extension:
            return extension[ext]
        elif fname in file:
            return file[fname]
        elif 'time' in fname.lower() or 'timing' in fname.lower():
            # hopeful test for timing files
            return cls.TIMING
        elif '-trackOrbit.dat' in fname:
            return cls.TRACK_ORBIT
        else:
            return cls.NONE
