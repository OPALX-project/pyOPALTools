# Author:   Matthias Frey
# Date:     April 2019

import re
import numpy as np

class LossParser:
    
    def __init__(self):
        
        self._names = [ 'element' ]
        
        self._units = { 'element': '' }
        
        self._dataset = []
        
    
    def parse(self, filename):
        """
        Example:
        1. Clean:
        ---------
        line = "# Element STQ1 x (mm),  y (mm),  z (mm),  px ( ),  py ( ),  pz ( ), id,  turn,  time (ns)"
        
        gets
        
        line = " x (mm),  y (mm),  z (mm),  px ( ),  py ( ),  pz ( ), id,  turn,  time (ns)"
        
        2. no commas:
        ------------
        line = " x (mm),  y (mm),  z (mm),  px ( ),  py ( ),  pz ( ), id,  turn,  time (ns)"
        
        gets
        
        line = " x (mm)   y (mm)   z (mm)   px ( )   py ( )   pz ( )  id   turn   time (ns)"
        """
        line = ''
        
        # 4. April 2019
        # https://stackoverflow.com/questions/1904394/read-only-the-first-line-of-a-file
        with open(filename) as f:
            line = f.readline()
        
        # 1. step
        line = re.sub(r"# Element (\S+)", ' ', line)
        
        # 2. step
        line = re.sub(r',', ' ', line)
        
        # 3. step
        pattern = '(\\w+) (\\(\\w+\\))?'
        
        quantities = re.findall(pattern, line)
        
        dtypes = [ ('element', str) ] # change to 'unicode' for Python 3.6
        
        
        for quan in quantities:
            self._names.append( quan[0] )
            unit = quan[1].replace(')', '')
            unit = unit.replace('(', '')
            self._units[quan[0]] = unit
            
            dtypes.append( (quan[0], float) )
        
        self._dataset = np.genfromtxt(filename,
                                      comments='#',
                                      dtype=dtypes)
    
    def getDataOfVariable(self, var):
        if var in self._names:
            return self._dataset[var]
        else:
            raise RuntimeError("No variable '" + var + "' in dataset.")
    
    
    def getUnitOfVariable(self, var):
        if var in self._names:
            return self._units[var]
        else:
            raise RuntimeError("No variable '" + var + "' in dataset.")
    
    
    def isVariable(self, var):
        return var in self._names
    
    
    def getVariableNames(self):
        return self._names
    
    @property
    def size(self):
        return len(self._dataset)
