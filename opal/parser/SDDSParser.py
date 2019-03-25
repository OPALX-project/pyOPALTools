# Author:   Matthias Frey
# Date:     March 2018

import numpy as np
import re,os,sys

class SDDSParser:
    
    def parse(self, filename):
        self._nParameters = 0
        self._nColumns = 0
        self._nRows = 0
        self._i = 0
        
        self.variables = {}
        self._units = {}
        self.__description = {}
        
        # check file version
        version = self._checkVersion(filename)
        
        # parse header
        if version >= 10900:
            self._parseHeader1_9(filename)
        else:
            self._parseHeader1_6(filename)
        
        # read data
        self._dataset = np.genfromtxt(filename, skip_header = self._nRows, dtype=np.float64)
    
    def _checkVersion(self, filename):
        
        pattern = 'OPAL (.*) git'
        
        v = 0
        
        with open(filename) as f:
            for line in f:
                if 'OPAL' and 'git rev.' in line:
                    line = line.replace('#', '')
                    obj = re.match(pattern, line)
                    v = self._version(obj.group(1))
                    break;
        return v
                    
    
    def _version(self, v):
        digits = v.split('.')
        
        i1 = int(digits[0]) * 10000
        i2 = int(digits[1]) * 100
        return i1 + i2
        
    
    def _parseHeader1_6(self, filename):
        column_pattern = '&columnname=(.*),type=(.*),units=(.*),description=\"(.*)\"&end'
        #parameter_pattern = '&parametername=(.*),type=(.*),description=\"(.*)\"&end'
        
        with open(filename) as f:
            for line in f:
                self._nRows += 1
                line = line.replace(' ', '')
                if 'SDDS' in line:
                    continue
                elif 'column' in line:
                    self._nRows += 1
                    obj = re.match(column_pattern, line)
                    self.variables[obj.group(1)] = self._nColumns
                    self._units[self._nColumns] = obj.group(3)
                    self.__description[self._nColumns] = self.__removeNumber(obj.group(4))
                    self._nColumns += 1
                elif 'parameter' in line:
                    self._nRows += 1
                    self._nParameters += 1
                elif 'description' in line:
                    self._nRows += 1
                elif 'data' in line:
                    self._nRows += 1
                else:
                    self._nRows += self._nParameters - 1
                    break
    
    
    def _parseHeader1_9(self, filename):
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
    
    # returns a column
    def getDataOfVariable(self, varname):
        return list(self._dataset[:, self.variables[varname]])
    
    
    def getUnitOfVariable(self, varname):
        return self._units[self.variables[varname]]
    
    
    def getVariables(self):
        return list(self.variables.keys())
    
    def getDescriptionOfVariable(self, varname):
        return self.__description[self.variables[varname]]
    
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
                self.__description[self._nColumns] = self.__removeNumber(line[line.find('=')+2:-2])
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
    
    def __removeNumber(self, s):
        # 25. March 2019
        # https://stackoverflow.com/questions/12851791/removing-numbers-from-string
        return ''.join([i for i in s if not i.isdigit()])

    def collectStatFileData(self, baseFN, root, yNames):

        ''' 
        Assumes runOPAL structure: optLinac_40nC_IBF=485.9269768907996_IM ...
        where baseFN == optLinac_40nC in the example above.

        This function finds all stat files that are one level
        below root. An exclude list can be specified.
 
        Two vectors are returned: x with the design variables names and values 
        (IBF=485.9269768907996 ... from above) and the last value(s) of stat 
        file data spcified via yNames.

        Example: 
        x        = []
        y        = []
        baseFN   = 'optLinac_40nC'
        exclList = ['tmpl','extrData.py']
        root     = "."
        yNames   = ['s','energy']
        p        = SDDSParser()
        (x,y)    = p.makeData(baseFN, exclList, root, yNames)
        '''

        x       = []
        y       = []
        fns     = [] # full qualified file names

        for item in filter(os.path.isdir, os.listdir(root)): # os.listdir(root):
            s = item.replace(baseFN+'_', '')
            s = s.replace('_', ' ')
            x.append(s)
            fn=item+'/'+baseFN+'.stat'
            if (os.path.isfile(fn)):
                self.parse(fn)
                yy = []
                for name in yNames:
                    yy.append(self.getDataOfVariable(name))
                y.append(yy)
                fns.append(fn)
            else:
                print ('file '+fn+' does not exists')
        return (x,y,fns)
    
    
    @property
    def size(self):
        return np.shape(self._dataset)[0]
