# Author:   Matthias Frey
# Date:     May 2018

import os
from opal.parser.sampler import SamplerParser
from .DatasetBase import DatasetBase
from opal.visualization.SamplerPlotter import SamplerPlotter
from opal.analysis.SamplerStatistics import SamplerStatistics
from string import digits
from opal.utilities.logger import opal_logger

class SamplerDataset(DatasetBase, SamplerPlotter, SamplerStatistics):
    '''
    :ivar __parser: actual data holder
    :vartype __parser: SamplerParser
    :ivar __nFiles: number of sampler output files found
    :vartype __nFiles: int
    '''
    
    def __init__(self, directory, fname):
        """
        Constructor.
        
        :param directory: directory name
        :type directory: str
        :param fname: generation file name
        :type fname: str
        """
        super(SamplerDataset, self).__init__(directory, fname)
        
        self.__parser = SamplerParser()
        
        self.__nFiles = 0
        self._loaded_file = -1
        
        for f in os.listdir(directory):
            if f.endswith(".json"):
                full_path = os.path.join(directory, f)
                if self.__parser.check_file(full_path):
                    self.__nFiles += 1
        
        opal_logger.info( 'Sampler dataset consisting of ' +
                          str(self.__nFiles) + ' files.' )
        
    
    
    def __load_file(self, ind):
        """
        A sampler output might be split into several files.
        This function first checks if new data needs to be loaded and
        then reads the data if necessary.
        
        :param ind: individual identity number
        :type ind: int
        """
        
        if self._loaded_file >= 0 and \
           ind >= self.__parser.begin and \
           ind <= self.__parser.end:
               # already loaded
               opal_logger.debug( 'already loaded' )
               return
        
        # search appropriate file
        end = self.__nFiles - 1
        if ind < self.__parser.begin:
            end = self._loaded_file - 1
        
        beg = 0
        if ind > self.__parser.end:
            beg = self._loaded_file + 1
        
        for i in range(beg, end+1):
            opal_logger.debug( 'load ' + str(i) )
            self.__actual_file_load(i)
            self._loaded_file = i
            if self.__parser.num_samples > 0 and \
               ind >= self.__parser.begin and \
               ind <= self.__parser.end:
                   break
    
    
    def __actual_file_load(self, i):
        import re
        fname = self.filename
        base  = os.path.basename(fname)
        dirname = os.path.dirname(fname)
        pattern = r'.*_(\d+).json'
        obj = re.match(pattern, base)
        num = obj.group(1)
        base = base.replace(num + '.json', '')
        self.__parser.parse(os.path.join(dirname,
                                         base + \
                                         num + '.json'))
    
    
    def getData(self, var, **kwargs):
        """
        Obtain the input data of a design variable
        of an individual. In order to select a specific
        individual set parameter 'ind' >= 0. If 'ind'
        is not given, the function takes the default value 0.
        
        :param var: a design variable or objective
                        if ``var == ''`` the full dvar (``dvar==True``) or
                        objective data is returned
        :type var: str
        
        :param ind: individual identity number (default: 0) (optional)
        :type ind: int
        :param dvar: return DVAR data in case of var==''
                        (default: True) (optional)
        :type dvar: bool
        
        :returns: design variable simulation input value.
        """
        try:
            ind   = kwargs.get('ind', 0)
            dvar  = kwargs.get('dvar', True)
            
            self.__load_file(ind)
            
            if var == '':
                if dvar:
                    return self.__parser.getIndividual(ind)
                else:
                    return self.__parser.getObjectives(ind)
            
            if var in self.__parser.design_variables:
                return self.__parser.getIndividual(ind)[var]
            elif var in self.__parser.objectives:
                return self.__parser.getObjectives(ind)[var]
            else:
                raise ValueError("The variable '" + var + "' is not in dataset.")
        except Exception as ex:
            opal_logger.exception(ex)
            return []
    
    
    def getLabel(self, var):
        """
        Obtain label for plotting.
        
        :param var: variable name
        :type var: str
        
        :returns: appropriate name plotting ready
        """
        try:
            if self._loaded_file < 0:
                self.__load_file(0)
            
            if not var in self.__parser.design_variables:
                raise ValueError("The variable '" + var + "' is not in dataset.")
            
            return var
        except Exception as ex:
            opal_logger.exception(ex)
            return ''
    
    
    def getUnit(self, var):
        """
        Obtain unit for plotting.
        
        **Note:**
        
        The sampler does not yet write the units
        of each variable to the files. This function
        raises an error.
        
        :param var:   variable name
        :type var: str
        :returns: None
        """
        
        try:
            #FIXME
            raise RuntimeError("The sampler does not yet provide units.")
        except Exception as ex:
            opal_logger.exception(ex)
            return ''
        
        return
    
    
    @property
    def design_variables(self):
        """
        Obtain design variable names
        """
        if self._loaded_file < 0:
            self.__load_file(0)
        
        return self.__parser.design_variables
    
    
    @property
    def objectives(self):
        """
        Obtain objectives names
        """
        if self._loaded_file < 0:
            self.__load_file(0)
        
        return self.__parser.objectives
    
    
    @property
    def bounds(self):
        """
        Obtain design variable upper and lower bounds
        """
        if self._loaded_file < 0:
            self.__load_file(0)
        
        return self.__parser.bounds
    
    
    @property
    def size(self):
        """
        Returns the number of individuals
        """
        if self.__nFiles == 0:
            return 0
        
        n = 0
        for i in range(self.__nFiles):
            self.__actual_file_load(i)
            n += self.__parser.num_samples
        return n


    def __str__(self):
        self.__load_file(0)
        s  = '\n\tSampler dataset.\n\n'
        s += '\tNumber of optimizers:  ' + str(self.__nFiles) + '\n\n'
        s += '\tNumber of samples: ' + str(self.size) + ' per generation \n\n'
        s += '\tAvailable design variables (' + str(len(self.design_variables)) + ') :\n\n'
        for v in sorted(self.design_variables):
            s += '\t' + '%-20s' % (v) + '\n'
        s += '\n\tAvailable objectives (' + str(len(self.objectives)) + ') :\n\n'
        for v in sorted(self.objectives):
            s += '\t' + '%-20s' % (v) + '\n'
        return s
