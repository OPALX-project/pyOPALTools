# Author:   Matthias Frey
# Date:     May 2018

import re
import numpy as np

class HistogramParser:
    """
    Parses *.hist files of OPAL that are written for probe
    elements and *.hist files of measurements.
    
    The first line in both files is a comment line starting with
    '#'. The measurement header line should be
    
    # Histogram bin counts (radius ['unit'], intensity ['unit'])
    
    where a simulation header is
    
    # Histogram bin counts (min, max, nbins, binsize) \
        'min' 'unit' 'max' 'unit' '#bins' 'binsize 'unit'
    
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
        
        simulation_pattern = r'# Histogram bin counts \((\w+), (\w+), (\w+), (\w+)\) (.*) (\w+) (.*) (\w+) (\d+) (.*) (\w+)'
        measurement_pattern = r'# Histogram bin counts \((\w+) \[(\w+)\], (\w+) \[(\w+)\]\)'
        
        match = False
        
        # measurement file
        radius  = None
        runit   = None
        current = None
        cunit   = None
        
        with open(filename) as f:
            for line in f:
                if '#' in line:
                    # 24. March
                    # https://stackoverflow.com/questions/2077897/substitute-multiple-whitespace-with-single-whitespace-in-python
                    line = ' '.join(line.split())
                    obj = re.match(simulation_pattern, line)
                    
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
                    
                    obj = re.match(measurement_pattern, line)
                    if obj:
                        radius  = obj.group(1)
                        runit   = obj.group(2)
                        current = obj.group(3)
                        cunit   = obj.group(4)
                        
                        match = True
                        
                    else:
                        break
        
        if not match:
            raise RuntimeError('Not proper file format.')
        
        
        if not radius == None:
            # measurement file
            r, c = np.loadtxt(filename, skiprows=1, usecols=(0,1), unpack=True)
            self._info['nbins'] = [len(r), '']
            self._info['min'] = [min(r), runit]
            self._info['max'] = [max(r), runit]
            
            self._info['binsize'] = [
                (self._info['max'][0] - self._info['min'][0]) / self._info['nbins'][0],
                runit
            ]
            
            self._info['bincount'].append( c )
        
        else:
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
