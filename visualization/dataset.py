import os
from enum import IntEnum, unique
from utilities.H5Parser import H5Parser
from utilities.SDDSParser import SDDSParser
from timing.Timing import Timing

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
        else:
            return cls.NONE


def load_dataset(directory, **kwargs):
    
    if not os.path.exists(directory):
        raise RuntimeError("No such directory: '" + directory + "'.")
    
    ftype = kwargs.get('ftype', FileType.NONE)
    fname = kwargs.get('fname', '')
    
    if not ftype == FileType.NONE and fname:
        raise RuntimeError('Specify either file type or file name but not both.')
    
    if fname:
        if not os.path.exists(directory + '/' + fname):
            raise RuntimeError("File '" + directory + "/" + fname + "' does not exist.")
        return Dataset(directory, [fname])
    elif not ftype == FileType.NONE:
        
        files = []
        
        for fname in os.listdir(directory):
            if FileType.extensionToFileType(fname) == ftype:
                files.append(fname)
        
        if not files:
            raise RuntimeError('Could not find any files of this type.')
        
        return Dataset(directory, files)
        
    else:
        print ( "Neither file type 'ftype' nor file name 'fname' specified." )
        print ( 'Try loading stat file.' )
        load_dataset(directory, ftype=FileType.STAT)


class Dataset:
    
    def __init__(self, directory, files):
        self.__directory = directory + '/'
        self.__files = files
        self.__ftype = FileType.extensionToFileType(files[0])
        self.__parser = []
        
        print ( self.__str__() )
        
        print ( 'Start loading files ...\n' )
        for f in files:
            print ( '    ' + f )
            if self.__ftype == FileType.H5:
                self.__parser.append(H5Parser())
                self.__parser[-1].parse(self.__directory + f)
            elif self.__ftype == FileType.STAT:
                self.__parser.append(SDDSParser())
                self.__parser[-1].parse(self.__directory + f)
            elif self.__ftype == FileType.TIMING:
                self.__parser.append(Timing())
                self.__parser[-1].read_ippl_timing(self.__directory + f)
        
        print ( '\nDone.\n' )
    
    
    def __str__(self):
        info = '\nAvailable files:\n'
        for f in self.__files:
            if not f == '':
                info += '    ' + f    + '\n'     
        return info
    
    
    @property
    def filetype(self):
        return self.__ftype
    
    
    def __getitem__(self, idx):
        return self.__parser[idx]
    
    
    def filename(self, idx):
        return self.__directory + self.__files[idx]
    
    @property
    def size(self):
        return len(self.__files)
    
    
    def getData(self, idx, **kwargs):
        """
        
        Returns
        -------
        the data of a parsed file
        """
        xvar = kwargs.get('xvar', '')
        yvar = kwargs.get('yvar', '')
        zvar = kwargs.get('zvar', '')
        
        if self.__ftype == FileType.TIMING:
            return self.__parser[idx].getTiming()
        elif self.__ftype == FileType.H5:
            
            step = kwargs.get('step', 0)
            
            xdata = []
            if xvar:
                xdata = self.__parser[idx].getStepDataset(xvar, step)
            
            ydata = []
            if yvar:
                ydata = self.__parser[idx].getStepDataset(yvar, step)
            
            zdata = []
            if zvar:
                zdata = self.__parser[idx].getStepDataset(zvar, step)
                
            return xdata, ydata, zdata
        
        elif self.__ftype == FileType.STAT:
            xdata = []
            if xvar:
                xdata = self.__parser[idx].getDataOfVariable(xvar)
            
            ydata = []
            if yvar:
                ydata = self.__parser[idx].getDataOfVariable(yvar)
            
            zdata = []
            if zvar:
                zdata = self.__parser[idx].getDataOfVariable(zvar)
            
            
            return xdata, ydata, zdata
    
    def getUnit(self, idx, **kwargs):
        xvar = kwargs.get('xvar', '')
        yvar = kwargs.get('yvar', '')
        zvar = kwargs.get('zvar', '')
        
        if self.__ftype == FileType.TIMING:
            return None
        elif self.__ftype == FileType.H5:
            
            step = kwargs.get('step', 0)
            
            xunit = ''
            if xvar:
                xunit = self.__parser[idx].getGlobalAttribute(xvar + 'Unit')
            
            yunit = ''
            if yvar:
                yunit = self.__parser[idx].getGlobalAttribute(yvar + 'Unit')
            
            zunit = ''
            if zvar:
                zunit = self.__parser[idx].getGlobalAttribute(zvar + 'Unit')
            
            return xunit, yunit, zunit
            
        elif self.__ftype == FileType.STAT:
            xunit = ''
            if xvar:
                xunit = self.__parser[idx].getUnitOfVariable(xvar)
            
            yunit = ''
            if yvar:
                yunit = self.__parser[idx].getUnitOfVariable(yvar)
            
            zunit = ''
            if zvar:
                zunit = self.__parser[idx].getDataOfVariable(zvar)
            
            return xunit, yunit, zunit
