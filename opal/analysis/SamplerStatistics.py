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

class SamplerStatistics:

    def find_matches(self, ids1, ids2, **kwargs):
        """Compare two lists

        Compare two lists with indices `ids1` and `ids2` in order to check
        if they are independent (i.e. not many matches).

        Parameters
        ----------
        ids1 : list
            Indices of 1st sample set
        ids2 : list
            Indices of 2nd sample set
        matches : bool, optional
            If true, the input values of the matches are
            returned as well, (default: False)

        Returns
        -------
        int
            Number of matches
        list
            Values of matched input (only if `matches` is True)
        """
        ndvars = len(self.ds.design_variables)

        nmatches = 0
        matches = []
        for i in ids1:
            pt1 = list(self.ds.getData(var='', dvar=True, ind=i).values())
            for j in ids2:
                pt2 = list(self.ds.getData(var='', dvar=True, ind=j).values())
                # 11. April 2019
                # https://stackoverflow.com/questions/1388818/how-can-i-compare-two-lists-in-python-and-return-matches
                match = [k for k, l in zip(pt1, pt2) if k == l]

                if len(match) == ndvars:
                    nmatches += 1
                    matches.append(match)

        if kwargs.pop('matches', False):
            return nmatches, matches
        return nmatches
