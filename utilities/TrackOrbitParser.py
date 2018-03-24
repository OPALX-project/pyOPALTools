# Author:   Matthias Frey
# Date:     March 2018

import numpy as np

class TrackOrbitParser:
    
    def __init__(self):
        
        self._names = [ 'ID', 'x', 'px', 'y', 'py', 'z', 'pz' ]
        
        self._units = {
            self._names[0]:   '1',
            self._names[1]:   'mm',
            self._names[2]:   r'\beta\gamma',
            self._names[3]:   'mm',
            self._names[4]:   r'\beta\gamma',
            self._names[5]:   'mm',
            self._names[6]:   r'\beta\gamma'
        }
        
        self._dataset = []
        
    
    def parse(self, filename):
        
        pattern =  '# Part. ID x [mm] beta_x*gamma '
        pattern += 'y [mm] beta_y*gamma z [mm] beta_z*gamma'
        
        match = False
        
        with open(filename) as f:
            for line in f:
                if '#' in line:
                    # 24. March
                    # https://stackoverflow.com/questions/2077897/substitute-multiple-whitespace-with-single-whitespace-in-python
                    line = ' '.join(line.split())
                    if line == pattern:
                        match = True
                else:
                    break
        
        if not match:
            raise RuntimeError('Not proper file format.')
        
        self._dataset = np.genfromtxt(filename,
                                      comments='#',
                                      delimiter = ' ',
                                      dtype=[(self._names[0], 'S3'), # change to 'unicode' for Python 3.6
                                             (self._names[1], np.float64),
                                             (self._names[2], np.float64),
                                             (self._names[3], np.float64),
                                             (self._names[4], np.float64),
                                             (self._names[5], np.float64),
                                             (self._names[6], np.float64)]
                                      )
        
        for i in range(len(self._dataset[self._names[0]])):
            self._dataset[self._names[0]][i] = self._dataset[self._names[0]][i][-1:]
    
    def getDataOfVariable(self, var):
        
        if var == self._names[0]:
            # 23. March
            # https://stackoverflow.com/questions/39371467/numpy-loadtxt-returns-string-repr-of-bytestring-instead-of-string
            return self._dataset[self._names[0]].astype('int')
        elif var in self._names:
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
