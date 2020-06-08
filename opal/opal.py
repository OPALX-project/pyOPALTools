# Copyright (c) 2018 - 2019, Matthias Frey, Paul Scherrer Institut, Villigen PSI, Switzerland
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

from .datasets.filetype import FileType
from .datasets.AmrDataset import AmrDataset
from .datasets.H5Dataset import H5Dataset
from .datasets.StatDataset import StatDataset
from .datasets.TimeDataset import TimeDataset
from .datasets.MemoryDataset import MemoryDataset
from .datasets.LBalDataset import LBalDataset
from .datasets.GridDataset import GridDataset
from .datasets.SolverDataset import SolverDataset
from .datasets.TrackOrbitDataset import TrackOrbitDataset
from .datasets.StdOpalOutputDataset import StdOpalOutputDataset
from .datasets.PeakDataset import PeakDataset
from .datasets.ProbeHistDataset import ProbeHistDataset
from .datasets.OptimizerDataset import OptimizerDataset
from .datasets.SamplerDataset import SamplerDataset
from .datasets.LossDataset import LossDataset
from .datasets.FieldDataset import FieldDataset

from .utilities.logger import opal_logger

# make it easier to use,
# avoids to do 'from opal.datasets.filetype import FileType'
filetype = FileType

def load_dataset(directory, **kwargs):
    """Load any file(s) produced by an OPAL simulation.

    If neither ftype nor fname is specified it tries to
    read in a ``*.stat`` file.

    Parameters
    ----------
    directory : str
        Root directory of the OPAL simulation
    ftype : FileType, optional
        Type of file to read in
    fname : str or tuple, optional
        File(s) to read in
    astype : FileType, optional
        Read a file according some dataset type
        E.g. OPAL standard output contains timings
        as well.
    """
    try:
        if not os.path.exists(directory):
            raise RuntimeError("No such directory: '" + directory + "'.")

        ftype  = kwargs.get('ftype', FileType.NONE)
        fname  = kwargs.get('fname', '')
        astype = kwargs.get('astype', FileType.NONE)

        if not ftype == FileType.NONE and fname:
            raise RuntimeError('Specify either file type or file name but not both.')

        fnames = []

        if isinstance(fname, str) and not fname == '':
            opal_logger.debug('Loading single file')
            full_path = os.path.join(directory, fname)
            if not os.path.exists(full_path):
                raise RuntimeError("File '" + full_path + "' does not exist.")
            fnames.append(fname)

        elif isinstance(fname, list) or isinstance(fname, tuple):
            opal_logger.debug('Loading list/tuple of files')
            for file in fname:
                full_path = os.path.join(directory, file)
                if not os.path.exists(full_path):
                    raise RuntimeError("File '" + full_path + "' does not exist.")
                fnames.append(file)
        elif not ftype == FileType.NONE:
            opal_logger.debug('Loading files of given file type')
            for fname in os.listdir(directory):
                full_path = os.path.join(directory, fname)
                if FileType.extensionToFileType(full_path) == ftype:
                    fnames.append(fname)

            if not fnames:
                raise RuntimeError('Could not find any files of this type.')
        else:
            opal_logger.error( "Neither file type 'ftype' nor file name 'fname' specified." )

        opal_logger.debug('Start loading files ...')
        datasets = []
        for fname in fnames:
            full_path = os.path.join(directory, fname)
            ftype = FileType.extensionToFileType(full_path)

            if  ftype == FileType.H5:
                datasets.append(H5Dataset(directory, fname))
                opal_logger.debug('    ' + fname + ' matches H5 file type.')
            elif ftype == FileType.STAT:
                datasets.append(StatDataset(directory, fname))
                opal_logger.debug('    ' + fname + ' matches stat file type.' )
            elif ftype == FileType.SMB:
                datasets.append(StatDataset(directory, fname))
                opal_logger.debug('    ' + fname + ' matches smb file type.' )
            elif ftype == FileType.TIMING:
                datasets.append(TimeDataset(directory, fname, 'ippl'))
                opal_logger.debug('    ' + fname + ' matches timing file type.' )
            elif ftype == FileType.OUTPUT:
                if astype == FileType.TIMING:
                    datasets.append(TimeDataset(directory, fname, 'output'))
                    opal_logger.debug('    ' + fname + ' matches timing file type.' )
                else:
                    datasets.append(StdOpalOutputDataset(directory, fname))
                    opal_logger.debug('    ' + fname + ' matches OPAL standard output file type.' )
            elif ftype == FileType.MEM:
                datasets.append(MemoryDataset(directory, fname))
                opal_logger.debug('    ' + fname + ' matches memory file type.' )
            elif ftype == FileType.LBAL:
                datasets.append(LBalDataset(directory, fname))
                opal_logger.debug('    ' + fname + ' matches load balancing file type.' )
            elif ftype == FileType.GRID:
                datasets.append(GridDataset(directory, fname))
                opal_logger.debug('    ' + fname + ' matches grid file type.' )
            elif ftype == FileType.SOLVER:
                datasets.append(SolverDataset(directory, fname))
                opal_logger.debug('    ' + fname + ' matches solver file type.' )
            elif ftype == FileType.TRACK_ORBIT:
                datasets.append(TrackOrbitDataset(directory, fname))
                opal_logger.debug('    ' + fname + ' matches track orbit file type.' )
            elif ftype == FileType.PEAK:
                datasets.append(PeakDataset(directory, fname))
                opal_logger.debug('    ' + fname + ' matches peak file type.' )
            elif ftype == FileType.HIST:
                datasets.append(ProbeHistDataset(directory, fname))
                opal_logger.debug('    ' + fname + ' matches probe histogram file type.' )
            elif ftype == FileType.OPTIMIZER:
                datasets.append(OptimizerDataset(directory, fname))
                # after reading we leave since optimizer produces many files
                opal_logger.debug('    ' + fname + ' matches optimizer file type. Stop reading further.' )
                break
            elif ftype == FileType.SAMPLER:
                datasets.append(SamplerDataset(directory, fname))
                opal_logger.debug('    ' + fname + ' matches sampler file type.' )
                break
            elif ftype == FileType.AMR:
                datasets.append(AmrDataset(directory))
                opal_logger.debug('    ' + directory + ' matches AMR file type.' )
                break
            elif ftype == FileType.LOSS:
                datasets.append(LossDataset(directory, fname))
                opal_logger.debug('    ' + fname + ' matches loss file type.' )
            elif ftype == FileType.FIELD:
                datasets.append(FieldDataset(directory, fname))
                opal_logger.debug('    ' + fname + ' matches field file type.' )
            elif ftype == FileType.NONE:
                opal_logger.error('no appropriate file match.' )
        opal_logger.debug('\nDone.\n' )

        if not datasets:
            raise RuntimeError('No dataset loaded.')
        elif len(datasets) == 1:
            return datasets[0]
        else:
            return datasets
    except Exception as ex:
        opal_logger.error(ex)
