# Copyright (c) 2018, 2020, Matthias Frey, Paul Scherrer Institut, Villigen PSI, Switzerland
# All rights reserved
#
# Implemented as part of the PhD thesis
# "Precise Simulations of Multibunches in High Intensity Cyclotrons"
#
# This file is part of pyOPALTools.
#
# pyOPALTools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# You should have received a copy of the GNU General Public License
# along with pyOPALTools. If not, see <https://www.gnu.org/licenses/>.

import os
from enum import IntEnum, unique

from opal.parser.sampler import SamplerParser
from opal.parser.OptimizerParser import OptimizerParser

from opal.utilities.logger import opal_logger

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
    OPTIMIZER   = 11,
    SAMPLER     = 12,
    SMB         = 13,
    AMR         = 14,
    LOSS        = 15,
    NONE        = 16

    @classmethod
    def extensionToFileType(cls, fname):
        opal_logger.debug('FileType.extensionToFileType: Check file type')
        extension = {
            '.h5':      cls.H5,
            '.stat':    cls.STAT,
            '.smb':     cls.SMB,
            '.mem':     cls.MEM,
            '.lbal':    cls.LBAL,
            '.out':     cls.OUTPUT,
            '.output':  cls.OUTPUT,
            '.grid':    cls.GRID,
            '.solver':  cls.SOLVER,
            '.peaks':   cls.PEAK,
            '.hist':    cls.HIST,
            '.json':    [cls.OPTIMIZER, cls.SAMPLER],
            '.loss':    cls.LOSS
        }

        file = {
            'timing.dat':       cls.TIMING,
            '-trackOrbit.dat':  cls.TRACK_ORBIT
        }

        _ , ext = os.path.splitext(fname)

        if ext in extension:
            # FIXME not nice file handling
            # currently only JSON could be for
            # OPTIMIZER or SAMPLER --> try parsing
            # if no exception is raised, it's a SAMPLER file
            if isinstance(extension[ext], list):
                opal_logger.debug('FileType.extensionToFileType: Optimizer or sampler output')
                try:
                    parser = SamplerParser()
                    optparser = OptimizerParser()
                    if parser.check_file(fname):
                        return cls.SAMPLER
                    elif optparser.check_file(fname):
                        return cls.OPTIMIZER
                    else:
                        return cls.NONE
                except:
                    return cls.NONE
            else:
                return extension[ext]
        elif fname in file:
            return file[fname]
        elif 'time' in fname.lower() or 'timing' in fname.lower():
            # hopeful test for timing files
            return cls.TIMING
        elif '.o' in fname:
            return cls.OUTPUT
        elif '-trackOrbit.dat' in fname:
            return cls.TRACK_ORBIT
        elif os.path.basename(fname) == 'Header':
            return cls.AMR
        else:
            return cls.NONE
