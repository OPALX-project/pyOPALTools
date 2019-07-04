# Author:   Matthias Frey
# Date:     March 2018

import os
from opal.parser.TrackOrbitParser import TrackOrbitParser
from .DatasetBase import DatasetBase
from opal.visualization.TrackOrbitPlotter import TrackOrbitPlotter
from opal.analysis.TrackOrbitAnalysis import TrackOrbitAnalysis
import numpy as np
from opal.utilities.logger import opal_logger

class TrackOrbitDataset(DatasetBase, TrackOrbitPlotter, TrackOrbitAnalysis):
    
    def __init__(self, directory, fname):
        """
        Constructor.
        
        Members
        -------
        __parser            (TrackOrbitParser)  actual data holder
        __unit_label_mapper ([])                map units of variables
                                                to plotting style
        """
        super(TrackOrbitDataset, self).__init__(directory, fname)
        
        self.__parser = TrackOrbitParser()
        self.__parser.parse(self.filename)
        
        self.__unit_label_mapper = [
            'x',
            'y',
            'z'
        ]
    
    
    def getData(self, var, **kwargs):
        """
        Obtain the data of a variable
        
        Parameters
        ----------
        var     (str)   variable name
        
        Returns
        -------
        an array of the dataself
        """
        return np.asarray(self.__parser.getDataOfVariable(var))
    
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
        try:
            if self.__parser.isVariable(var):
                return var
            else:
                raise RuntimeError("No variable '" + var + "' in dataset.")
        except Exception as ex:
            opal_logger.exception(ex)
            return ''

    
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
            if not self.__parser.isVariable(var):
                raise RuntimeError("No variable '" + var + "' in dataset.")
            
            unit = self.__parser.getUnitOfVariable(var)
            if var in self.__unit_label_mapper:
                unit = r'\mathrm{' + unit + '}'
            
            return r'$' + unit + '$'
        except Exception as ex:
            opal_logger.exception(ex)
            return ''


    @property
    def size(self):
        return self.__parser.size
    
    
    def __str__(self):
        s  = '\n\tTrack Orbit dataset.\n\n'
        variables = self.__parser.getVariableNames()
        s += '\tSize: ' + str(len(variables)) + ' x ' + str(self.size) + '\n\n'
        s += '\tAvailable variables (' + str(len(variables)) + ') :\n\n'
        for v in sorted(variables):
            s += '\t' + '%-20s' % (v) + '\t' + '%-25s' % (self.__parser.description[v]) + \
                 '\t' + self.__parser.getUnitOfVariable(v) + '\n'
        return s
