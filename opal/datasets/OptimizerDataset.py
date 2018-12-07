# Author:   Matthias Frey
# Date:     May 2018

import os
from opal.parser.OptimizerParser import OptimizerParser
from opal.datasets.DatasetBase import *
from string import digits

class OptimizerDataset(DatasetBase):
    
    def __init__(self, directory, fname):
        """
        Constructor.
        
        Parameters
        ----------
        directory           (str)                   directory name
        fname               (str)                   generation file name
        
        Members
        -------
        __parser            (OptimizerParser)       actual data holder
        __postfix           (str)                   substring of generation
                                                    filenames that is
                                                    identical to all files
        _loaded_generation  (int)                   currently loaded generation
        _loaded_optimizer   (int)                   currently loaded optimizer
        _loadedGeneration   (function)              load a generation file
        """
        
        full_path = os.path.join(directory, fname)
        if not os.path.exists(full_path):
            raise ValueError("File '" + full_path + "' does not exist.")
        
        self.__parser = OptimizerParser(directory)

        self.__postfix = '_' + str.split(fname, "_", 2)[1] + '_'
        
        self._loaded_generation = -1
        self._loaded_optimizer = -1
        
        self._loadGeneration( int( str.split(fname, "_", 1)[0] ) )
        
        super(OptimizerDataset, self).__init__(directory, fname)
    
    
    def getData(self, var, **kwargs):
        """
        Obtain the data of a variable or all data
        of an individual. An individual is returned
        when setting 'ind' > 0. In that case the
        'var' parameter is not considered.
        
        Parameters
        ----------
        var     (str)   a design variable
                        or objective
        
        Optionals
        ---------
        ind     (int)   individual identity number
        gen     (int)   generation, default: 1
        opt     (int)   optimizer, default: 0
        all     (bool)  get all info of an individual
                        (i.e. objectives, design variables)
        
        Returns
        -------
        an array of the data
        """
        gen = kwargs.get('gen', 1)
        opt = kwargs.get('opt', 0)
        
        al = kwargs.get('all', True)
        
        self._loadGeneration(gen, opt)
        
        ind = kwargs.get('ind', -1)
        
        if not ind == -1 and al:
            return self.__parser.getIndividualWithID(ind)
        
        if not var in self.objectives and \
            not var in self.design_variables:
                raise ValueError("The variable '" + var + "' is not in dataset.")
        
        if ind == -1:
            if var in self.objectives:
                idx = self.objectives.index(var)
                return self.__parser.getAllOutput()[:, idx]
            else:
                idx = self.design_variables.index(var)
                return self.__parser.getAllInput()[:, idx]
        else:
            if var in self.objectives:
                idx = self.objectives.index(var)
                iidx = self.__parser.getIndexOfID(ind)
                return self.__parser.getAllOutput()[iidx, idx]
            else:
                idx = self.design_variables.index(var)
                iidx = self.__parser.getIndexOfID(ind)
                return self.__parser.getAllInput()[iidx, idx]
    
    
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
        if not var in self.objectives and \
            not var in self.design_variables:
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
        raise RuntimeError("The optimizer does not yet provide units.")
        
        return
    
    
    def getGenerationBasename(self, gen, opt=0):
        """
        Obtain the basename of a specific
        generation.
        
        Parameters
        ----------
        gen         (int)   generation
        opt         (int)   optimizer number (default: 0)
        
        Returns
        -------
        a basename of the selected generation
        """
        
        maxgen = self.__parser.getNumOfGenerations()
        
        if gen < 1 or gen > maxgen:
            raise ValueError('Generation number negative or ' +
                             'greater than ' + str(maxgen) + '.')
        
        
        genfile = str(gen) + self.__postfix + str(opt) + '.json'
        filename = os.path.join(self._directory, genfile)
        
        if not os.path.isfile(filename):
            raise IOError("File '" + filename + "' does not exist.")
        
        return genfile
    
    
    @property
    def objectives(self):
        """
        Obtain objective names
        """
        return self.__parser.getObjectives()
    
    @property
    def design_variables(self):
        """
        Obtain design variable names
        """
        return self.__parser.getDesignVariables()
    
    
    @property
    def num_generations(self):
        """
        Obtain the number of generations
        """
        return self.__parser.getNumOfGenerations()
    
    
    @property
    def bounds(self):
        """
        Obtain design variable upper and lower bounds
        """
        return self.__parser.getBounds()
    
    
    def individuals(self, gen, opt=0):
        """
        Obtain the ID of every individual of the
        currently loaded generation file
        
        Parameters
        ----------
        gen         (int)   generation
        opt         (int)   optimizer (default: 0)
        """
        self._loadGeneration(gen, opt)
        
        return self.__parser.getIDs()
    
    
    def _loadGeneration(self, gen, opt=0):
        """
        Load data of generation into memory.
        
        Parameters
        ----------
        gen         (int)   generation
        opt         (int)   optimizer (default: 0)
        
        Returns
        -------
        None
        """
        if not gen == self._loaded_generation or \
            not opt == self._loaded_optimizer:
            self.__parser.readGeneration(gen, opt)
            self._loaded_generation = gen
            self._loaded_optimizer = opt
