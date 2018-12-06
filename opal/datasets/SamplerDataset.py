# Author:   Matthias Frey
# Date:     May 2018

import os
from opal.parser.sampler import SamplerParser
from opal.datasets.DatasetBase import *
from string import digits

class SamplerDataset(DatasetBase):
    
    def __init__(self, directory, fname):
        """
        Constructor.
        
        Parameters
        ----------
        directory           (str)                   directory name
        fname               (str)                   generation file name
        
        Members
        -------
        __parser            (SamplerParser)         actual data holder
        __nFiles            (int)                   number of sampler output files found
        """
        
        full_path = os.path.join(directory, fname)
        
        base = str.split(fname, '_')[0]
        
        if not os.path.exists(full_path):
            raise ValueError("File '" + full_path + "' does not exist.")
        
        self.__parser = SamplerParser()
        
        self.__nFiles = 0
        self._loaded_file = -1
        
        for f in os.listdir(directory):
            if f.endswith(".json"):
                full_path = os.path.join(directory, f)
                if self.__parser.check_file(full_path):
                    self.__nFiles += 1
        
        print ( 'Sampler dataset consisting of ' +
                str(self.__nFiles) + ' files.' )
        
        super(SamplerDataset, self).__init__(directory, fname)
    
    
    def __load_file(self, ind):
        """
        A sampler output might be split into several files.
        This function first checks if new data needs to be loaded and
        then reads the data if necessary.
        
        Parameters
        ----------
        ind     (int)   individual identity number
        """
        
        if self._loaded_file >= 0 and \
           ind >= self.__parser.begin and \
           ind <= self.__parser.end:
               # already loaded
               print ( 'already loaded' )
               return
        
        # search appropriate file
        end = self.__nFiles - 1
        if ind < self.__parser.begin:
            end = self._loaded_file - 1
        
        beg = 0
        if ind > self.__parser.end:
            beg = self._loaded_file + 1
        
        for i in range(beg, end+1):
            fname = self.filename
            base  = os.path.basename(fname)
            dirname = os.path.dirname(fname)
            split = str.split(base, '_', 2)
            print ( 'load ' + str(i) )
            self.__parser.parse(os.path.join(dirname,
                                             split[0] + '_' + \
                                             split[1] + '_' + \
                                             str(i) + '.json'))
            self._loaded_file = i
            if self.__parser.num_samples > 0 and \
               ind >= self.__parser.begin and \
               ind <= self.__parser.end:
                   break
    
    
    def getData(self, var, **kwargs):
        """
        Obtain the input data of a design variable
        of an individual. In order to select a specific
        individual set parameter 'ind' >= 0. If 'ind'
        is not given, the function takes the default value 0.
        
        Parameters
        ----------
        var     (str)   a design variable
        
        Optionals
        ---------
        ind     (int)   individual identity number
        
        Returns
        -------
        design variable simulation input value.
        """
        ind = kwargs.get('ind', 0)
        
        self.__load_file(ind)
        
        if not var in self.__parser.design_variables:
            raise ValueError("The variable '" + var + "' is not in dataset.")
        
        return self.__parser.getIndividual(ind)[var]
    
    
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
        if self._loaded_file < 0:
            raise RuntimeError('No dataset loaded yet.')
        
        if not var in self.__parser.design_variables:
            raise ValueError("The variable '" + var + "' is not in dataset.")
        
        return var
    
    
    def getUnit(self, var):
        """
        Obtain unit for plotting.
        
        Note: The optimizer does not yet write the units
              of each variable to the files. This function
              raises an error.
        
        Parameters
        ----------
        var     (str)   variable name
        
        Returns
        -------
        None
        """
        
        #FIXME
        raise RuntimeError("The sampler does not yet provide units.")
        
        return
    
    
    @property
    def design_variables(self):
        """
        Obtain design variable names
        """
        if self._loaded_file < 0:
            raise RuntimeError('No dataset loaded yet.')
        
        return self.__parser.design_variables
    
    
    @property
    def bounds(self):
        """
        Obtain design variable upper and lower bounds
        """
        if self._loaded_file < 0:
            raise RuntimeError('No dataset loaded yet.')
        
        return self.__parser.bounds
