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
    
    It is also able to readd simulation files of the same form.
    
    Members
    -------
    self._peaks = {
            'type':     simulation or measurement
            'name':     list of all supported variables
            'dataset':  list of radii and intensity
            'unit':     list of units
    }
    """
    
    def __init__(self):
        
        self._peaks = {
            'type':     '',
            'name':     [],
            'dataset':  [],
            'unit':     []
        }
    
    def parse(self, filename):
        
        measurement_pattern =  r'# Peak Radii \((\w+)\), (.*), (\d+) (\w+) \((.*)\)'
        simulation_pattern = r'# Peak Radii \((\w+)\)'
        
        match = False
        
        with open(filename) as f:
            for line in f:
                if '#' in line:
                    # 24. March
                    # https://stackoverflow.com/questions/2077897/substitute-multiple-whitespace-with-single-whitespace-in-python
                    line = ' '.join(line.split())
                    obj = re.match(measurement_pattern, line)
                    if obj:
                        self._peaks['type'] = 'measurement'
                        
                        # intensity
                        self._peaks['name'].append( 'intensity' )
                        self._peaks['unit'].append( obj.group(4) )                        
                        self._peaks['dataset'].append( obj.group(3) )
                        
                        # radii
                        self._peaks['name'].append( 'radii' )
                        self._peaks['unit'].append( obj.group(1) )
                        
                        match = True
                    
                    obj = re.match(simulation_pattern, line)
                    if obj:
                        self._peaks['type'] = 'simulation'
                        
                        # radii
                        self._peaks['name'].append( 'radii' )
                        self._peaks['unit'].append( obj.group(1) )

                        match = True
                    else:
                        break
        
        if not match:
            raise RuntimeError('Not proper file format.')
        
        self._peaks['dataset'].append( np.genfromtxt(filename,
                                                     comments='#',
                                                     delimiter = ' ',
                                                     dtype=np.float64
                                                     )
        )
    
    
    def getDataOfVariable(self, var):
        if not self.isVariable(var):
            raise ValueError("No variable '" + var + "' in dataset.")
        
        idx = self._peaks['name'].index(var)
        return self._peaks['dataset'][idx]
    
    
    def getUnitOfVariable(self, var):
        if not self.isVariable(var):
            raise ValueError("No variable '" + var + "' in dataset.")
        
        idx = self._peaks['name'].index(var)
        return self._peaks['unit'][idx]
    
    
    def isVariable(self, var):
        return var in self._peaks['name']
    
    
    def getVariableName(self):
        return self._peaks['name']
    
    def getType(self):
        return self._peaks['type']
