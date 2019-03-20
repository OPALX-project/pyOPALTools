# Author:   Matthias Frey
# Date:     March 2018

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
    fname           (str)       file to read in (optional)
    astype          (FileType)  read a file according some dataset type
                                E.g. OPAL standard output contains timings
                                as well.
    """
    
    if not os.path.exists(directory):
        raise RuntimeError("No such directory: '" + directory + "'.")
    
    ftype  = kwargs.get('ftype', FileType.NONE)
    fname  = kwargs.get('fname', '')
    astype = kwargs.get('astype', FileType.NONE)
    info   = kwargs.get('info', True)
    
    if not ftype == FileType.NONE and fname:
        raise RuntimeError('Specify either file type or file name but not both.')
    
    fnames = []
    
    if fname:
        full_path = os.path.join(directory, fname)
        if not os.path.exists(full_path):
            raise RuntimeError("File '" + full_path + "' does not exist.")        
        fnames.append(fname)
    elif not ftype == FileType.NONE:
        for fname in os.listdir(directory):
            full_path = os.path.join(directory, fname)
            if FileType.extensionToFileType(full_path) == ftype:
                fnames.append(fname)
        
        if not fnames:
            raise RuntimeError('Could not find any files of this type.')
    else:
        print ( "Neither file type 'ftype' nor file name 'fname' specified." )
        print ( 'Try loading stat file.' )
        load_dataset(directory, ftype=FileType.STAT)
    
    
    print ( 'Start loading files ...\n' )
    datasets = []
    for fname in fnames:
        if info:
            print ( '    ' + fname + ' ... ', end='' )
        full_path = os.path.join(directory, fname)
        ftype = FileType.extensionToFileType(full_path)
        
        if  ftype == FileType.H5:
            datasets.append(H5Dataset(directory, fname))
            if info:
                print ( 'matches H5 file type.' )
        elif ftype == FileType.STAT:
            datasets.append(StatDataset(directory, fname))
            if info:
                print ( 'matches stat file type.' )
        elif ftype == FileType.SMB:
            datasets.append(StatDataset(directory, fname))
            if info:
                print ( 'matches smb file type.' )
        elif ftype == FileType.TIMING:
            datasets.append(TimeDataset(directory, fname, 'ippl'))
            if info:
                print ( 'matches timing file type.' )
        elif ftype == FileType.OUTPUT:
            if astype == FileType.TIMING:
                datasets.append(TimeDataset(directory, fname, 'output'))
                if info:
                    print ( 'matches timing file type.' )
            else:
                datasets.append(OutputDataset(directory, fname))
                if info:
                    print ( 'matches OPAL standard output file type.' )
        elif ftype == FileType.MEM:
            datasets.append(MemoryDataset(directory, fname))
            if info:
                print ( 'matches memory file type.' )
        elif ftype == FileType.LBAL:
            datasets.append(LBalDataset(directory, fname))
            if info:
                print ( 'matches load balancing file type.' )
        elif ftype == FileType.GRID:
            datasets.append(GridDataset(directory, fname))
            if info:
                print ( 'matches grid file type.' )
        elif ftype == FileType.SOLVER:
            datasets.append(SolverDataset(directory, fname))
            if info:
                print ( 'matches solver file type.' )
        elif ftype == FileType.TRACK_ORBIT:
            datasets.append(TrackOrbitDataset(directory, fname))
            if info:
                print ( 'matches track orbit file type.' )
        elif ftype == FileType.PEAK:
            datasets.append(PeakDataset(directory, fname))
            if info:
                print ( 'matches peak file type.' )
        elif ftype == FileType.HIST:
            datasets.append(ProbeHistDataset(directory, fname))
            if info:
                print ( 'matches probe histogram file type.' )
        elif ftype == FileType.OPTIMIZER:
            datasets.append(OptimizerDataset(directory, fname))
            # after reading we leave since optimizer produces many files
            if info:
                print ( 'matches optimizer file type. Stop reading further.' )
            break
        elif ftype == FileType.SAMPLER:
            datasets.append(SamplerDataset(directory, fname))
            if info:
                print ( 'matches sampler file type.' )
            break
        elif ftype == FileType.NONE:
            if info:
                print ( 'no appropriate file match.' )
    print ( '\nDone.\n' )
    
    return datasets
