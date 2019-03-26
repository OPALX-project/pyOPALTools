# Author:   Matthias Frey
# Date:     March 2018

from opal.parser.SDDSParser import SDDSParser
from opal.datasets.DatasetBase import *
import numpy as np

class SDDSDatasetBase(DatasetBase):
    
    def __init__(self, directory, fname, **kwargs):
        """
        Constructor.
        
        Members
        ----------
        _parser            (SDDSParser)    actual data holder
        _variable_mapper   (dict)          map user input variable
                                           name to file variable name
        _label_mapper      (dict)          map user input variable
                                           name to plot label name
        _unit_label_mapper ([])            map units of variables
                                           to plotting style
        """
        self._parser = SDDSParser()
        
        full_path = os.path.join(directory, fname)
        if not os.path.exists(full_path):
            raise RuntimeError("File '" + full_path + "' does not exist.")
        
        self._parser.parse(full_path)
        
        self._variable_mapper = kwargs.pop('variable_mapper', {})
        
        self._label_mapper  = kwargs.pop('label_mapper', {})
        
        self._unit_label_mapper = kwargs.pop('unit_label_mapper', [])
        
        self._dataset_type = kwargs.pop('dataset_type', 'No')
        
        self._print_limit = kwargs.pop('print_limit', -1)
        
        super(SDDSDatasetBase, self).__init__(directory, fname)
    
    def getData(self, var, **kwargs):
        """
        Obtain data of a variable
        
        Parameters
        ----------
        var     (str)   variable name
        
        Returns
        -------
        a list of the data
        """
        sddsvar = var
        
        if var in self._variable_mapper:
            sddsvar = self._variable_mapper[var]
        
        if not sddsvar in self._parser.getVariables():
            raise RuntimeError("The variable '" + var + "' is not in dataset.")
        return np.asarray(self._parser.getDataOfVariable(sddsvar))
    
    
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
        sddsvar = var
        
        if var in self._variable_mapper:
            sddsvar = self._variable_mapper[var]
        
        if not sddsvar in self._parser.getVariables():
            raise RuntimeError("The variable '" + var + "' is not in dataset.")
        
        if var in self._label_mapper:
            var = self._label_mapper[var]
        
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
        sddsvar = var
        
        if var in self._variable_mapper:
            sddsvar = self._variable_mapper[var]
            
        if not sddsvar in self._parser.getVariables():
            raise RuntimeError("The variable '" + var + "' is not in dataset.")
        
        unit = self._parser.getUnitOfVariable(sddsvar)
        
        if var in self._unit_label_mapper:
            unit = r'\mathrm{' + unit + '}'
        
        return r'$' + unit + '$'


    def getVariables(self):
        """
        Obtain all variables within file.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        list of strings
        """
        return self._parser.getVariables()


    @property
    def size(self):
        return self._parser.size


    def __str__(self):
        variables = sorted(self._parser.getVariables())
        nvar = len(variables)
        s  = '\n\t' + self._dataset_type + ' dataset.\n\n'
        s += '\tSize: ' + str(nvar) + ' x ' + str(self.size) + '\n\n'
        s += '\tAvailable variables (' + str(nvar) + ') :\n\n'
        if self._print_limit < nvar:
            for v in variables:
                s += '\t' + '%-20s' % (v) + '\t' + self._parser.getDescriptionOfVariable(v) + '\n'
        else:
            s += '\t' + '%-20s' % (variables[0]) + '\t' + self._parser.getDescriptionOfVariable(variables[0]) + '\n'
            s += '\t' + '%-20s' % (variables[1]) + '\t' + self._parser.getDescriptionOfVariable(variables[1]) + '\n'
            s += '\t' + '%-20s' % (variables[2]) + '\t' + self._parser.getDescriptionOfVariable(variables[2]) + '\n'
            s += '\t...\n'
            s += '\t' + '%-20s' % (variables[-2]) + '\t' + self._parser.getDescriptionOfVariable(variables[-2]) + '\n'
            s += '\t' + '%-20s' % (variables[-1]) + '\t' + self._parser.getDescriptionOfVariable(variables[-1]) + '\n'
        return s
