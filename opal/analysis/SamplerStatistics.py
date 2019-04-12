import numpy as np

class SamplerStatistics:

    def find_matches(self, ids1, ids2, **kwargs):
        """
        Compare two lists of indices ids1 and ids2
        in order to check if they are independent (i.e. not many matches).
        
        Parameters
        ----------
        ids1        (list)  indices of 1st sample set
        ids2        (list)  indices of 2nd sample set
        
        Optional
        --------
        matches     (bool)  if true, the input values of the matches are
                            returned as well
        
        Returns
        -------
        number of matches
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
