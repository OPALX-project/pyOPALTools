# Author:   Matthias Frey
# Date:     May 2018

import re
import numpy as np

class PeakParser:
    """
    Read measurement file of the form:
    
    # Peak Radii (mm), 18 June 2008, 200 uA (RRI2-65)
    2103.8
    2122.4
    2140.4
    2159.8
    2180.8
    2201.8
    2224.6
    2247.8
    2270.0
    2287.8
    2302.6
    2315.6
    2331.4
    2356.0
    2379.6
    2403.6
    2424.6
    
    Members
    -------
    self._names     ([str])     all supported variables
    self._intensity (float)     current where measurement was
                                performed
    self._units     ([str])     all units
    self._dataset   ([float)]   radii
    """
    
    def __init__(self):
        
        self._names = ['radii', 'intensity']
        self._intensity = 0.0
        
        self._units = ['', '']
        
        self._dataset = []
        
    
    def parse(self, filename):
        
        pattern =  r'# Peak Radii \((\w+)\), (.*), (\d+) (\w+) \((.*)\)'
        
        match = False
        
        with open(filename) as f:
            for line in f:
                if '#' in line:
                    # 24. March
                    # https://stackoverflow.com/questions/2077897/substitute-multiple-whitespace-with-single-whitespace-in-python
                    line = ' '.join(line.split())
                    obj = re.match(pattern, line)
                    if obj:
                        self._units[0] = obj.group(1)
                        self._intensity = obj.group(3)
                        self._units[1] = obj.group(4)
                        match = True
                else:
                    break
        
        if not match:
            raise RuntimeError('Not proper file format.')
        
        self._dataset = np.genfromtxt(filename,
                                      comments='#',
                                      delimiter = ' ',
                                      dtype=np.float64
                                      )
    
    def getDataOfVariable(self, var):
        
        if not var in self._names:
            raise ValueError("No variable '" + var + "' in dataset.")
        
        idx = self._names.index(var)
        
        if idx == 0:
            return self._dataset
        else:
            return self._intensity
    
    
    def getUnitOfVariable(self, var):
        if not var in self._names:
            raise ValueError("No variable '" + var + "' in dataset.")
        idx = self._names.index(var)
        return self._units[idx]
    
    
    def isVariable(self, var):
        return var in self._names
