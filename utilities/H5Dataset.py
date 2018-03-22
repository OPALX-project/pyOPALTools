# Author:   Matthias Frey
# Date:     March 2018

from utilities.H5Parser import H5Parser
import numpy as np

class H5Dataset:
    
    def __init__(self, directory, fname):
        """
        Constructor.
        
        Members
        ----------
        __directory         (str)           of file
        __fname             (str)           name of file
        __parser            (H5Parser)      actual data holder
        __variable_mapper   (dict)          map user input variable
                                            name to file variable name
        __label_mapper      (dict)          map user input variable
                                            name to plot label name
        __direction         (dict)          used to find out the
                                            direction in case of
                                            vector type data
        """
        self.__directory = directory
        self.__fname = fname
        
        self.__parser = H5Parser()
        self.__parser.parse(directory + fname)
        
        self.__variable_mapper = {
            'rms_x':    'RMSX',
            'rms_y':    'RMSX',
            'rms_z':    'RMSX',
            'rms_px':   'RMSP',
            'rms_py':   'RMSP',
            'rms_pz':   'RMSP',
            'time':     'TIME',
            'energy':   'ENERGY',
            's':        'SPOS'
        }
        
        self.__label_mapper  = {
            'rms_x':    r'$\sigma_x$',
            'rms_y':    r'$\sigma_y$',
            'rms_z':    r'$\sigma_z$',
            'rms_px':   r'$\sigma_{px}$',
            'rms_py':   r'$\sigma_{py}$',
            'rms_pz':   r'$\sigma_{pz}$'
        }
        
        self.__direction = {
            'x':    0,
            'y':    1,
            'z':    2
        }
    
    
    def getData(self, var, step):
        """
        Obtain data of a variable
        
        Parameters
        ----------
        var     (str)   variable name
        step    (int)   in case of step variables
        
        Returns
        -------
        a list of the data (n, dim)
        """
        
        h5var = var
        if var in self.__variable_mapper:
            h5var = self.__variable_mapper[var]
        
        if h5var in self.__parser.getStepDatasets(step):
            return self.__parser.getStepDataset(h5var, step)
        elif h5var in self.__parser.getStepAttributes(step):
            data = []
            
            # if vector type we need to get appropriate direction
            dim = 0
            for key in self.__direction:
                if '_' + key in var:
                    dim = self.__direction[key]
                elif '_p' + key in var:
                    dim = self.__direction[key]
            
            for i in range(self.__parser.getNSteps()):
                data.append(self.__parser.getStepAttribute(h5var, i)[dim])
            
            return data
        else:
            raise H5Error("'" + var + "' is not part of this step")
    
    
    def getLabel(self, var):
        """
        Obtain label for plotting.
        
        Parameters
        ----------
        var     (str)   variable name
        
        Returns
        -------
        appropriate name plotting ready
        """
        if var in self.__label_mapper:
            var = self.__label_mapper[var]
        return var
    
    def getUnit(self, var):
        """
        Obtain unit for plotting.
        
        Parameters
        ----------
        var     (str)   variable name
        
        Returns
        -------
        appropriate unit in math mode for plotting 
        """
        if var in self.__variable_mapper:
            var = self.__variable_mapper[var]
        
        unit = self.__parser.getGlobalAttribute(var + 'Unit')
        unit = unit.replace('#', '\\')
        unit = r'$' + unit + '$'
        return unit
