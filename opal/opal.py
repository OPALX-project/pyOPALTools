import os
from opal.datasets.DatasetBase import *
from opal.datasets.H5Dataset import H5Dataset
from opal.datasets.StatDataset import StatDataset
from opal.datasets.TimeDataset import TimeDataset


def load_dataset(directory, **kwargs):
    
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
            datasets.append(TimeDataset(directory, fname))
            print ( 'matches timing file type.' )
        elif ftype == FileType.NONE:
            print ( 'no appropriate file match.' )
    print ( '\nDone.\n' )
    
    return datasets
