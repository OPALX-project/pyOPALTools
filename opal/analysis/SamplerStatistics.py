from opal.utilities.logger import opal_logger
import numpy as np

class SamplerStatistics:
    
    def find_matches(self, train, **kwargs):
        """
        Compare training and validation set in order to check
        if they are independent (i.e. not many matches).
        
        Parameters
        ----------
        train       (list)  the indices of the training points
        
        Optional
        --------
        matches     (bool)  if true, the input values of the matches are
                            returned as well
        
        Returns
        -------
        number of matches
        """
        nsamples = self.ds.size
        ntrain = len(train)
        
        if ntrain >= nsamples:
            opal_logger.error('ntrain (' + str(ntrain) + ') >= ' +
                              'nsamples (' + str(nsamples) + ')')
        
        ndvars = len(self.ds.design_variables)
        
        validation = np.arange(nsamples, dtype=int)
        
        # 12. April 2019
        # https://stackoverflow.com/questions/3428536/python-list-subtraction-operation
        validation = [int(i) for i in validation if int(i) not in train]
        
        nmatches = 0
        matches = []
        # loop over validation points
        for i in validation:
            val_pt = list(self.ds.getData(var='', dvar=True, ind=i).values())
            for j in train:
                train_pt = list(self.ds.getData(var='', dvar=True, ind=j).values())
                # 11. April 2019                                                                                              
                # https://stackoverflow.com/questions/1388818/how-can-i-compare-two-lists-in-python-and-return-matches        
                match = [k for k, l in zip(val_pt, train_pt) if k == l]
                
                if len(match) == ndvars:
                    nmatches += 1
                    matches.append(match)
        
        if kwargs.pop('matches', False):
            return nmatches, matches
        return nmatches
