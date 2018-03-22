# Author:   Matthias Frey
# Date:     March 2018

from utilities.SDDSParser import SDDSParser

class StatDataset:
    
    def __init__(self, directory, fname):
        self.__directory = directory
        self.__fname = fname
        
        self.__parser = SDDSParser()
        self.__parser.parse(directory + fname)
        
        self.__variable_mapper = {
            'time':     't',
        }
        
        self.__label_mapper  = {
            'rms_x':    r'$\sigma_x$',
            'rms_y':    r'$\sigma_y$',
            'rms_z':    r'$\sigma_z$',
            'rms_px':   r'$\sigma_{px}$',
            'rms_py':   r'$\sigma_{py}$',
            'rms_pz':   r'$\sigma_{pz}$'
        }
    
    
    def getData(self, var, step):
        if var in self.__variable_mapper:
            var = self.__variable_mapper[var]
        return self.__parser.getDataOfVariable(var)
    
    
    def getLabel(self, var):
        if var in self.__label_mapper:
            var = self.__label_mapper[var]
        return var
    
    
    def getUnit(self, var):
        if var in self.__variable_mapper:
            var = self.__variable_mapper[var]
        unit = r'$' + self.__parser.getUnitOfVariable(var) + '$'
        return unit
