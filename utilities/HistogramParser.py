# Author:   Matthias Frey
# Date:     May 2018

import re
import numpy as np

class HistogramParser:
    """
    Parses *.hist files of OPAL that are written for probe
    elements.
    
    Members
    -------
    self._info = {
            'min':       list of minimum value and unit
            'max':       list of maximum value and unit
            'nbins':     list of number of bins and unit
            'binsize':   list of size of bin and unit
            'bincount':  list of bin counts and unit
    }
    """
    
    def __init__(self):
        
        self._info = {
            'min':      [],
            'max':      [],
            'nbins':    [],
            'binsize':  [],
            'bincount': []
        }
    
    
    def parse(self, filename):
        
        pattern = r'# Histogram bin counts \((\w+), (\w+), (\w+), (\w+)\) (.*) (\w+) (.*) (\w+) (\d+) (.*) (\w+)'
        
        match = False
        
        with open(filename) as f:
            for line in f:
                if '#' in line:
                    # 24. March
                    # https://stackoverflow.com/questions/2077897/substitute-multiple-whitespace-with-single-whitespace-in-python
                    line = ' '.join(line.split())
                    obj = re.match(pattern, line)
                    
                    if obj:
                        j = 5
                        for i in range(1, 5):
                            key = obj.group(i)
                            if not key in self._info:
                                raise ValueError("Not able to read info '" + key + "' from header.") 
                            
                            if not key == 'nbins':
                                self._info[key].append( obj.group( j ) )     # value
                                self._info[key].append( obj.group( j + 1 ) ) # unit
                                j += 2
                            else:
                                # no unit
                                self._info[key].append( obj.group( j ) )
                                self._info[key].append( '' )
                                j += 1
                        
                        match = True
                    else:
                        break
        
        if not match:
            raise RuntimeError('Not proper file format.')
        
        self._info['bincount'].append( np.genfromtxt(filename,
                                                     comments='#',
                                                     delimiter = ' ',
                                                     dtype=np.float64
                                                     )
        )
        
        self._info['bincount'].append('')
    
    
    def getDataOfVariable(self, var):
        if not self.isVariable(var):
            raise ValueError("No variable '" + var + "' in dataset.")
        return self._info[var][0]
    
    
    def getUnitOfVariable(self, var):
        if not self.isVariable(var):
            raise ValueError("No variable '" + var + "' in dataset.")
        return self._info[var][1]
    
    
    def isVariable(self, var):
        return var in self._info
