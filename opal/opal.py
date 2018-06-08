# Author:   Matthias Frey
# Date:     March 2018

import os
import logging

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
from opal.datasets.ElementDataset import ElementDataset

def load_dataset(directory, **kwargs):
    """
    Load any file(s) produced by an OPAL simulation.
    If neither ftype nor fname is specified it tries to
    read in a *.stat file.

    To see stdoutput, use the python logging module like an adult
    
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
    
    if not os.path.exists(directory):
        raise RuntimeError("No such directory: '" + directory + "'.")
    
    ftype  = kwargs.get('ftype', FileType.NONE)
    fname  = kwargs.get('fname', '')
    astype = kwargs.get('astype', FileType.NONE)
    
    if not ftype == FileType.NONE and fname:
        raise RuntimeError('Specify either file type or file name but not both.')
    
    fnames = []

    if isinstance(fname,str):
        full_path = os.path.join(directory, fname)
        if not os.path.exists(full_path):
            raise RuntimeError("File '" + full_path + "' does not exist.")        
        fnames.append(fname)
    
    elif isinstance(fname,list) or isinstance(fname,tuple):
        for file in fname:
            full_path = os.path.join(directory, file)
            if not os.path.exists(full_path):
                raise RuntimeError("File '" + full_path + "' does not exist.")        
            fnames.append(file)
    
    elif not ftype == FileType.NONE:
        for file in os.listdir(directory):
            full_path = os.path.join(directory, file)
            if FileType.extensionToFileType(full_path) == ftype:
                fnames.append(file)
        
        if not fnames:
            raise RuntimeError('Could not find any files of this type.')
    else:
        logging.debug ( "Neither file type 'ftype' nor file name 'fname' specified." )
        logging.debug ( 'Try loading stat file.' )
        return load_dataset(directory, ftype=FileType.STAT)
    
    
    logging.info( 'Start loading files ...' )
    datasets = []
    
    for file in fnames:
        logging.info (file)
        full_path = os.path.join(directory, file)
        ftype = FileType.extensionToFileType(full_path)
        
        if  ftype == FileType.H5:
            datasets.append(H5Dataset(directory, file))
            logging.debug ( 'matches H5 file type.' )
        elif ftype == FileType.STAT:
            datasets.append(StatDataset(directory, file))
            logging.debug ( 'matches stat file type.' )
        elif ftype == FileType.TIMING:
            datasets.append(TimeDataset(directory, file, 'ippl'))
            logging.debug ( 'matches timing file type.' )
        elif ftype == FileType.OUTPUT:
            if astype == FileType.TIMING:
                datasets.append(TimeDataset(directory, file, 'output'))
                logging.debug ( 'matches timing file type.' )
            else:
                datasets.append(OutputDataset(directory, file))
                logging.debug ( 'matches OPAL standard output file type.' )
        elif ftype == FileType.MEM:
            datasets.append(MemoryDataset(directory, file))
            logging.debug ( 'matches memory file type.' )
        elif ftype == FileType.LBAL:
            datasets.append(LBalDataset(directory, file))
            logging.debug ( 'matches load balancing file type.' )
        elif ftype == FileType.GRID:
            datasets.append(GridDataset(directory, file))
            logging.debug ( 'matches grid file type.' )
        elif ftype == FileType.SOLVER:
            datasets.append(SolverDataset(directory, file))
            logging.debug ( 'matches solver file type.' )
        elif ftype == FileType.TRACK_ORBIT:
            datasets.append(TrackOrbitDataset(directory, file))
            logging.debug ( 'matches track orbit file type.' )
        elif ftype == FileType.PEAK:
            datasets.append(PeakDataset(directory, file))
            logging.debug ( 'matches peak file type.' )
        elif ftype == FileType.HIST:
            datasets.append(ProbeHistDataset(directory, file))
            logging.debug ( 'matches probe histogram file type.' )
        elif ftype == FileType.OPTIMIZER:
            datasets.append(OptimizerDataset(directory, file))
            # after reading we leave since optimizer produces many files
            logging.debug ( 'matches optimizer file type. Stop reading further.' )
            break
        elif ftype == FileType.SAMPLER:
            datasets.append(SamplerDataset(directory, file))
            logging.debug ( 'matches sampler file type.' )
            break
        elif ftype == FileType.ELEMENT:
            datasets.append(ElementDataset(directory, file))
            logging.debug( ' matches element file type')
        elif ftype == FileType.NONE:
            logging.debug ( 'no appropriate file match.' )
    logging.info ( 'Done.' )
    
    if len(datasets) == 1:
        return datasets[0]
    else:
        return datasets
