# Copyright (c) 2018, Matthias Frey, Paul Scherrer Institut, Villigen PSI, Switzerland
# All rights reserved
#
# Implemented as part of the PhD thesis
# "Precise Simulations of Multibunches in High Intensity Cyclotrons"
#
# This file is part of pyOPALTools.
#
# pyOPALTools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# You should have received a copy of the GNU General Public License
# along with pyOPALTools. If not, see <https://www.gnu.org/licenses/>.

import os
from opal.parser.OptimizerParser import OptimizerParser
from .DatasetBase import DatasetBase
from opal.visualization.OptimizerPlotter import OptimizerPlotter
from opal.analysis.OptimizerAnalysis import OptimizerAnalysis
from string import digits
from opal.utilities.logger import opal_logger

class OptimizerDataset(DatasetBase, OptimizerPlotter, OptimizerAnalysis):
    """
    Attributes
    ----------
    __parser : OptimizerParser
        Actual data holder
    __postfix : str
        Substring of generation
        filenames that is
        identical to all files
    _loaded_generation : int
        Currently loaded generation
    _loaded_optimizer : int
        Currently loaded optimizer
    _loadedGeneration : function
        Load a generation file

    """
    def __init__(self, directory, fname):
        """Constructor.

        Parameters
        ----------
        directory : str
            Directory name
        fname : str
            Generation file name
        """
        super(OptimizerDataset, self).__init__(directory, fname)

        self.__parser = OptimizerParser(directory)

        self.__parser.parse()

        self.__postfix = '_' + str.split(fname, "_", 2)[1] + '_'

        self._loaded_generation = -1
        self._loaded_optimizer = -1

        self._loadGeneration( int( str.split(fname, "_", 1)[0] ) )



    def getData(self, var, **kwargs):
        """Obtain the data of a variable or all data of an individual.

        An individual is returned
        when setting 'ind' > 0. In that case the
        'var' parameter is not considered.

        Parameters
        ----------
        var : str
            A design variable or objective
        ind : int, optional
            Individual identity number, default: -1, which means all
        gen: int, optional
            Generation, default: 1
        opt : int, optional
            Optimizer, default: 0
        all : bool, optional
            Get all info of an individual
            (i.e. objectives, design variables) default : True
        pareto :bool, optional
            Load pareto file (default: False)

        Returns
        -------
        array
            Array of the data
        """
        try:
            gen    = kwargs.get('gen', 1)
            opt    = kwargs.get('opt', 0)
            pareto = kwargs.get('pareto', False)

            al = kwargs.get('all', True)

            self._loadGeneration(gen, opt, pareto)

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
        except Exception as ex:
            opal_logger.exception(ex)
            return []


    def getLabel(self, var):
        """Obtain label for plotting.

        Parameters
        ----------
        var : str
            Variable name

        Returns
        -------
        str
            Appropriate name plotting ready
        """
        try:
            if not var in self.objectives and \
                not var in self.design_variables:
                raise ValueError("The variable '" + var + "' is not in dataset.")

            return var
        except Exception as ex:
            opal_logger.exception(ex)
            return ''


    def getUnit(self, var):
        """Obtain unit for plotting.

        Parameters
        ----------
        var : str
            Variable name

        Notes
        -----
        The optimizer does not yet write the units
        of each variable to the files. This function
        raises an error.
        """

        #FIXME
        try:
            raise RuntimeError("The optimizer does not yet provide units.")
        except Exception as ex:
            opal_logger.exception(ex)

        return ''


    def getGenerationBasename(self, gen, opt=0):
        """Obtain the basename of a specific generation.

        Parameters
        ----------
        gen : int
            Generation
        opt : int, optional
            Optimizer number (default: 0)

        Returns
        -------
        str
            A basename of the selected generation
        """
        try:
            maxgen = self.__parser.getNumOfGenerations()

            if gen < 1 or gen > maxgen:
                raise ValueError('Generation number negative or ' +
                                 'greater than ' + str(maxgen) + '.')

            genfile = str(gen) + self.__postfix + str(opt) + '.json'
            filename = os.path.join(self._directory, genfile)

            if not os.path.isfile(filename):
                raise IOError("File '" + filename + "' does not exist.")

            return genfile
        except Exception as ex:
            opal_logger.exception(ex)
            return ''


    @property
    def num_optimizers(self):
        return self.__parser.num_optimizers

    @property
    def objectives(self):
        """
        Obtain objective names
        """
        return self.__parser.getObjectives()

    @property
    def design_variables(self):
        """Obtain design variable names
        """
        return self.__parser.getDesignVariables()


    @property
    def num_generations(self):
        """Obtain the number of generations
        """
        return self.__parser.getNumOfGenerations()


    @property
    def bounds(self):
        """Obtain design variable upper and lower bounds
        """
        return self.__parser.getBounds()


    def individuals(self, gen, opt=0, pareto=False):
        """Obtain the ID of every individual of the currently loaded generation file

        Parameters
        ----------
        gen : int
            Generation
        opt : int, optional
            Optimizer (default: 0)
        pareto : bool, optional
            Load pareto file (default: False)
        """
        self._loadGeneration(gen, opt, pareto)

        return self.__parser.getIDs()


    def _loadGeneration(self, gen, opt=0, pareto=False):
        """Load data of generation into memory.

        Parameters
        ----------
        gen : int
            Generation
        opt : int, optional
            Optimizer (default: 0)
        pareto : bool, optional
            Load pareto file (default: False)
        """
        if pareto:
            self.__parser.readGeneration(-1, opt, pareto)
        elif not gen == self._loaded_generation or \
            not opt == self._loaded_optimizer:
            self.__parser.readGeneration(gen, opt)
            self._loaded_generation = gen
            self._loaded_optimizer = opt

    @property
    def size(self):
        """Returns the number of individuals
        """
        return len(self.individuals(1))


    def __str__(self):
        s  = '\n\tOptimizer dataset.\n\n'
        s += '\tNumber of optimizers:  ' + str(self.num_optimizers) + '\n\n'
        s += '\tNumber of generations: ' + str(self.num_generations) + '\n\n'
        s += '\tNumber of individuals: ' + str(self.size) + ' per generation \n\n'
        s += '\tAvailable design variables (' + str(len(self.design_variables)) + ') :\n\n'
        for v in sorted(self.design_variables):
            s += '\t' + '%-20s' % (v) + '\n'
        s += '\n\tAvailable objectives (' + str(len(self.objectives)) + ') :\n\n'
        for v in sorted(self.objectives):
            s += '\t' + '%-20s' % (v) + '\n'
        return s
