import os
from opal.datasets.DatasetBase import *
from opal.datasets.H5Dataset import H5Dataset
from opal.datasets.StatDataset import StatDataset
from opal.datasets.TimeDataset import TimeDataset
from opal.datasets.MemoryDataset import MemoryDataset
from opal.datasets.LBalDataset import LBalDataset
from opal.datasets.GridDataset import GridDataset
from opal.datasets.SolverDataset import SolverDataset
from opal.datasets.TrackOrbitDataset import TrackOrbitDataset


def load_dataset(directory, **kwargs):
    """
    Load any file(s) produced by an OPAL simulation.
    If neither ftype nor fname is specified it tries to
    read in a *.stat file.
    
    Parameters
    ----------
    directory       (str)       root directory of the OPAL simulation
    ftype           (FileType)  type of file to read in (optional)
    fname           (str)       file to read in (optional)
    """
    
    if not os.path.exists(directory):
        raise RuntimeError("No such directory: '" + directory + "'.")
    
    ftype = kwargs.get('ftype', FileType.NONE)
    fname = kwargs.get('fname', '')
    
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
            if FileType.extensionToFileType(fname) == ftype:
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
        print ( '    ' + fname + ' ... ', end='' )
        ftype = FileType.extensionToFileType(fname)
        if  ftype == FileType.H5:
            datasets.append(H5Dataset(directory, fname))
            print ( 'matches H5 file type.' )
        elif ftype == FileType.STAT:
            datasets.append(StatDataset(directory, fname))
            print ( 'matches stat file type.' )
        elif ftype == FileType.TIMING:
            datasets.append(TimeDataset(directory, fname, 'ippl'))
            print ( 'matches timing file type.' )
        elif ftype == FileType.OUTPUT:
            datasets.append(TimeDataset(directory, fname, 'output'))
            print ( 'matches timing file type.' )
        elif ftype == FileType.MEM:
            datasets.append(MemoryDataset(directory, fname))
            print ( 'matches memory file type.' )
        elif ftype == FileType.LBAL:
            datasets.append(LBalDataset(directory, fname))
            print ( 'matches load balancing file type.' )
        elif ftype == FileType.GRID:
            datasets.append(GridDataset(directory, fname))
            print ( 'matches grid file type.' )
        elif ftype == FileType.SOLVER:
            datasets.append(SolverDataset(directory, fname))
            print ( 'matches solver file type.' )
        elif ftype == FileType.TRACK_ORBIT:
            datasets.append(TrackOrbitDataset(directory, fname))
            print ( 'matches track orbit file type.' )
        elif ftype == FileType.NONE:
            print ( 'no appropriate file match.' )
    print ( '\nDone.\n' )
    
    return datasets
