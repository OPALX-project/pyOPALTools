import numpy as np

class SDDSParser:
    
    def parse(self, filename):
        self._nParameters = 0
        self._nColumns = 0
        self._nRows = 0
        self._i = 0
        
        self.variables = {}
        self._units = {}
        
        # parse header
        with open(filename) as f:
            for line in f:
                self._nRows += 1
                if 'SDDS' in line:
                    continue
                elif '&description' in line:
                    self._description(f)
                elif '&parameter' in line:
                    self._parameter(f)
                    self._nParameters += 1
                elif '&column' in line:
                    self._column(f)
                    self._nColumns += 1
                elif '&data' in line:
                    self._data(f)
                else:
                    self._nRows += self._nParameters - 1
                    break
        
        # read data
        self._dataset = np.genfromtxt(filename, skip_header = self._nRows, dtype=np.float64)
    
    
    # returns a column
    def getDataOfVariable(self, varname):
        return self._dataset[:, self.variables[varname]]
    
    
    def getUnitOfVariable(self, varname):
        return self._units[self.variables[varname]]
    
    
    def getVariables(self):
        return list(self.variables.keys())
    
    
    def _description(self, f):
        for line in f:
            self._nRows += 1
            if 'text' in line:
                pass
            elif 'contents' in line:
                pass
            elif '&end' in line:
                break
    
    
    def _parameter(self, f):
        for line in f:
            self._nRows += 1
            if 'name' in line:
                pass
            elif 'type' in line:
                pass
            elif 'description' in line:
                pass
            elif '&end' in line:
                break
    
    
    def _column(self, f):
        for line in f:
            self._nRows += 1
            if 'name' in line:
                self.variables[line[line.find('=')+1:-2]] = self._nColumns
                pass
            elif 'type' in line:
                pass
            elif 'units' in line:
                self._units[self._nColumns] = line[line.find('=')+1:-2]
            elif 'description' in line:
                pass
            elif '&end' in line:
                break
    
    
    def _data(self, f):
        for line in f:
            self._nRows += 1
            if 'mode' in line:
                pass
            elif 'no_row_counts' in line:
                pass
            elif '&end' in line:
                break
