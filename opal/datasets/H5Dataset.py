# Author:   Matthias Frey
# Date:     March 2018

import os
from opal.parser.H5Parser import H5Parser
from opal.parser.H5Error import *
from .DatasetBase import DatasetBase
from opal.visualization.H5Plotter import H5Plotter
from opal.analysis.H5Statistics import H5Statistics
from opal.utilities.logger import opal_logger
import numpy as np

import pandas as pd 

class H5Dataset(DatasetBase, H5Plotter, H5Statistics):
    
    def __init__(self, directory, fname):
        """
        Constructor.
        
        Members
        -------
        __parser            (H5Parser)      actual data holder
        __variable_mapper   (dict)          map user input variable
                                            name to file variable name
        __label_mapper      (dict)          map user input variable
        __unit_label_mapper ([])            map units of variables
                                            to plotting style
                                            name to plot label name
        __direction         (dict)          used to find out the
                                            direction in case of
                                            vector type data
        """
        super(H5Dataset, self).__init__(directory, fname)
        
        self.__parser = H5Parser()
        self.__parser.parse(self.filename)
        
        self.__variable_mapper = {
            'rms_x':        'RMSX',
            'rms_y':        'RMSX',
            'rms_z':        'RMSX',
            'rms_px':       'RMSP',
            'rms_py':       'RMSP',
            'rms_pz':       'RMSP',
            'time':         'time',
            'energy':       'ENERGY',
            's':            'SPOS',
            'flavour':      'OPAL_flavour'
        }
        
        self.__label_mapper  = {
            'rms_x':    r'$\sigma_x$',
            'rms_y':    r'$\sigma_y$',
            'rms_z':    r'$\sigma_z$',
            'rms_px':   r'$\sigma_{px}$',
            'rms_py':   r'$\sigma_{py}$',
            'rms_pz':   r'$\sigma_{pz}$'
        }
        
        self.__unit_label_mapper = [
            'rms_x',
            'rms_y',
            'rms_z',
            'x',
            'y',
            'z',
            'time'
        ]
        
        self.__direction = {
            'x':    0,
            'y':    1,
            'z':    2
        }
    
    
    def getData(self, var, **kwargs):
        """
        Obtain data of a variable
        
        Parameters
        ----------
        var     (str)   variable name
        
        Returns
        -------
        an array of the data (n, dim)
        """
        try:
            step = kwargs.get('step', 0)
        
            # take last step if negative
            if step < 0:
                step = self.__parser.getNSteps() - 1
        
            h5var = var
            if var in self.__variable_mapper:
                h5var = self.__variable_mapper[var]
        
            if h5var in self.__parser.getStepDatasets(step):
                return np.array(self.__parser.getStepDataset(h5var, step))
            elif h5var in self.__parser.getStepAttributes(step):
                data = []
            
                # if vector type we need to get appropriate direction
                if '_' in var:
                    dim = 0
                    for key in self.__direction:
                        if '_' + key in var:
                            dim = self.__direction[key]
                        elif '_p' + key in var:
                            dim = self.__direction[key]
                    
                    for i in range(self.__parser.getNSteps()):
                        data.append(self.__parser.getStepAttribute(h5var, i)[dim])
                else:
                    for i in range(self.__parser.getNSteps()):
                        
                        data.append(self.__parser.getStepAttribute(h5var, i))
                        
                        # get strings
                        if isinstance(data[-1], bytes):
                            data[-1] = data[-1].decode('utf-8')
                return np.asarray(data)
            else:
                raise H5Error("'" + var + "' is not part of this step")
        except Exception as ex:
            opal_logger.exception(ex)
            return []
    
    
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
        try:
            h5var = var
            
            if var in self.__variable_mapper:
                h5var = self.__variable_mapper[var]
            
            unit = self.__parser.getGlobalAttribute(h5var + 'Unit')
            unit = unit.replace('#', '\\')
            
            if var in self.__unit_label_mapper:
                unit = r'\mathrm{' + unit + '}'
            
            unit = r'$' + unit + '$'
            return unit
        except Exception as ex:
            opal_logger.exception(ex)
            return ''

    '''
    Experimental retruns Pandas data frames
    '''
    def getMonitorDataFrame(monData):
        cnames= ['id' ,'px', 'py', 'pz', 'time', 'turn', 'x', 'y', 'z']
        x = pd.DataFrame(columns=cnames)
        for v in cnames:
            x[v] = monData.getData(v)
        return x

    def getH5DataFrame(h5Data,s=0):
        cnames= ['id' ,'px', 'py', 'pz', 'ptype', 'x', 'y', 'z', 'q']
        x = pd.DataFrame(columns=cnames)
        for v in cnames:
            x[v] = h5Data.getData(v,step=s)
        return x


    @property
    def size(self):
        return self.__parser.getNSteps()


    def __str__(self):
        #variables = self.__parser.getVariables()
        s  = '\n\tH5 dataset.\n\n'
        s += '\tNumber of steps: ' + str(self.__parser.getNSteps())
        s += '\n\n\tAvailable step attributes (' + str(len(self.__parser.getStepAttributes())) + ')' + ':\n\n'
        for v in sorted(self.__parser.getStepAttributes()):
            s += '\t' + '%-20s' % (v) + '\n'
        s += '\n\n\tAvailable step datasets (' + str(len(self.__parser.getStepDatasets())) + ')' + ':\n\n'
        for v in sorted(self.__parser.getStepDatasets()):
            s += '\t' + '%-20s' % (v) + '\n'
        return s
