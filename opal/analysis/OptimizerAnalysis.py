# Copyright (c) 2019, Matthias Frey, Paul Scherrer Institut, Villigen PSI, Switzerland
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

import numpy as np

class OptimizerAnalysis:

    def find_minimum(self, exclude = [], constraints = {}):
        """Find the invidual with minimum sum of all objectives
        over all generations.

        It is possible to exclude some objectives with
        the list `exclude`.

        It is possible to give constraints on objectives as
        a dictionary, e.g. { "DPEAK_1_16": 4.0 } means only
        individuals that have a "DPEAK_1_16" objective with
        a value <= 4.

        Parameters
        ----------
        exclude : list, optional
            Objectives that should be excluded
        constraints: dict, optional
            Constraints on objectives

        Returns
        -------
        float
            Sum of objectives
        int
            Generation
        int
            Individual ID
        """
        gens = range(1, self.ds.num_generations + 1)
        objs = self.ds.objectives

        in_objs = []
        for obj in objs:
            if not obj in exclude:
                in_objs.append(obj)

        m = 1e15
        ind = -1
        gen = -1
        for g in gens:
            ids = self.ds.individuals(g)

            data = []
            for obj in in_objs:
                data.append( self.ds.getData(obj, gen=g) )

            data = np.asmatrix(data)

            for idx, ID in enumerate(ids):
                accept = True
                if constraints:
                    for k, o in enumerate(in_objs):
                        if o in constraints:
                            if data[k, idx] > constraints[o]:
                                accept = False

                if accept:
                    s = 0.0
                    for j, obj in enumerate(in_objs):
                        s += data[j, idx]
                    if s < m:
                        m = s
                        gen = g
                        ind = ID

        return m, gen, ind


    def find(self, function, opt=0):
        """Find the individual according to the given function in
        the Pareto file.

        Parameters
        ----------
        function : callable
            A function that takes all objectives
            of 2 individuals as values of 2 lists as argument and
            returns the better individual.
            The objectives are considered alphabetically ordered
        opt : int, optional
            Number of Pareto file

        Returns
        -------
        int
            The ID of best individual that fulfills the custom function.
        """
        ids = self.ds.individuals(gen=-1, opt=opt, pareto=True)
        objs = self.ds.objectives

        id_best = ids[0]
        ind1 = []
        for obj in objs:
            ind1.append( self.ds.getData(obj, ind=id_best, all=False,
                                         opt=opt, pareto=True) )

        for i in ids[1:]:
            ind2 = []
            for obj in objs:
                ind2.append( self.ds.getData(obj, ind=i, all=False,
                                             opt=opt, pareto=True) )
            ind = function(ind1, ind2)
            if ind == ind2:
                ind1 = ind
                id_best = i
        return id_best


    def print_individual(self, ind, gen=1, opt=0, pareto=False):
        """Print the values of the design variables and objectives of
        an individual.

        If pareto = True, gen is not considered.

        Parameters
        ----------
        ind : int
            Individual identity number
        gen : int, optional
            Generation, default: 1
        opt : int, optional
            Optimizer, default: 0
        pareto : bool, optional
            Load pareto file (default: False)
        """
        print ( "Design variables:" )
        dvars = self.ds.design_variables
        for dvar in dvars:
            print ( '\t', dvar, self.ds.getData(var=dvar, ind=ind, all=False,
                                                gen=gen, opt=opt, pareto=pareto) )

        objs  = self.ds.objectives
        if objs:
            print ( "Objectives:" )
            for obj in objs:
                print ( '\t', obj, self.ds.getData(var=obj, ind=ind, all=False,
                                                   gen=gen, opt=opt,
                                                   pareto=pareto) )
