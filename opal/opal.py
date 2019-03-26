# Author:   Matthias Frey
# Date:     March 2018 - 2019

import os

from opal.datasets.filetype import FileType
from opal.datasets.H5Dataset import H5Dataset
from opal.datasets.StatDataset import StatDataset
from opal.datasets.TimeDataset import TimeDataset
from opal.datasets.MemoryDataset import MemoryDataset
from opal.datasets.LBalDataset import LBalDataset
from opal.datasets.GridDataset import GridDataset
from opal.datasets.SolverDataset import SolverDataset
from opal.datasets.TrackOrbitDataset import TrackOrbitDataset
from opal.datasets.OutputDataset import OutputDataset
from opal.datasets.PeakDataset import PeakDataset
from opal.datasets.ProbeHistDataset import ProbeHistDataset
from opal.datasets.OptimizerDataset import OptimizerDataset
from opal.datasets.SamplerDataset import SamplerDataset

from opal.utilities.logger import opal_logger

def load_dataset(directory, **kwargs):
    """
    Load any file(s) produced by an OPAL simulation.
    If neither ftype nor fname is specified it tries to
    read in a *.stat file.

    Parameters
    ----------
    directory       (str)       root directory of the OPAL simulation
    
    Optionals
    ---------
    ftype           (FileType)  type of file to read in (optional)
    fname           (str/tuple) file(s) to read in (optional)
    astype          (FileType)  read a file according some dataset type
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
                    datasets.append(OutputDataset(directory, fname))
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
