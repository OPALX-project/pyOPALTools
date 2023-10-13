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

from opal.parser.FieldParser import FieldParser
from opal.parser.HistogramParser import HistogramParser
from opal.parser.H5Parser import H5Parser
from opal.parser.LossParser import LossParser
from opal.parser.OptimizerParser import OptimizerParser
from opal.parser.PeakParser import PeakParser
from opal.parser.sampler import SamplerParser
from opal.parser.SDDSParser import SDDSParser
from opal.parser.TimingParser import TimingParser
from opal.parser.TrackOrbitParser import TrackOrbitParser

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
    FIELD       = 16,
    NONE        = 17

    @classmethod
    def get_extensions(cls):
        extension = {
            '.h5':      [cls.H5],
            '.stat':    [cls.STAT],
            '.smb':     [cls.SMB],
            '.mem':     [cls.MEM],
            '.lbal':    [cls.LBAL],
            '.out':     [cls.OUTPUT],
            '.output':  [cls.OUTPUT],
            '.grid':    [cls.GRID],
            '.solver':  [cls.SOLVER],
            '.peaks':   [cls.PEAK],
            '.hist':    [cls.HIST],
            '.json':    [cls.OPTIMIZER, cls.SAMPLER],
            '.loss':    [cls.LOSS],
            '.dat':     [cls.FIELD, cls.TRACK_ORBIT, cls.TIMING]
        }
        return extension

    @classmethod
    def get_parsers(cls):
        parsers = {
            cls.H5:             H5Parser(),
            cls.STAT:           SDDSParser(),
            cls.SMB:            SDDSParser(),
            cls.MEM:            SDDSParser(),
            cls.LBAL:           SDDSParser(),
            cls.OUTPUT:         TimingParser(),
            cls.GRID:           SDDSParser(),
            cls.SOLVER:         SDDSParser(),
            cls.PEAK:           PeakParser(),
            cls.HIST:           HistogramParser(),
            cls.OPTIMIZER:      OptimizerParser(),
            cls.SAMPLER:        SamplerParser(),
            cls.LOSS:           LossParser(),
            cls.FIELD:          FieldParser(),
            cls.TIMING:         TimingParser(),
            cls.TRACK_ORBIT:    TrackOrbitParser()
        }
        return parsers

    @classmethod
    def extensionToFileType(cls, fname):
        opal_logger.debug('FileType.extensionToFileType: Check file type')
        extension = cls.get_extensions()
        parsers = cls.get_parsers()

        _ , ext = os.path.splitext(fname)
        if ext in extension.keys():
            for t in extension[ext]:
                try:
                    parser = parsers[t]
                    if parser.check_file(fname):
                        return t
                except:
                    pass
            return cls.NONE
        elif '.o' in fname:
            return cls.OUTPUT
        elif os.path.basename(fname) == 'Header':
            return cls.AMR
        else:
            return cls.NONE

    def checkFileType(cls, fname):
        _ , ext = os.path.splitext(fname)
        extension = cls.get_extensions()
        if cls == cls.AMR:
            return True
        elif not ext in extension.keys():
            return False

        parsers = cls.get_parsers()
        for t in extension[ext]:
            if t == cls:
                try:
                    parser = parsers[t]
                    if parser.check_file(fname):
                        return True
                except:
                    return False
        return False