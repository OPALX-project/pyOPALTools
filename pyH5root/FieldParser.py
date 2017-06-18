from enum import Enum
import numpy as np

class FieldType(Enum):
    SCALAR = 1
    VECTOR = 2

class FieldParser:
    
    def parse(self, filename):
        self._nx = 0
        self._ny = 0
        self._nz = 0
        self._data = []
        
        fieldtype = self._checkType(filename)
        
        if fieldtype == FieldType.SCALAR:
            self._parseScalarField(filename)
        elif fieldtype == FieldType.VECTOR:
            self._parseVectorField(filename)
        else:
            raise RuntimeError("Unknown field type.")
    
    
    def _parseScalarField(self, filename):
        self._data = np.genfromtxt(fname = filename,
                                   dtype=np.float64)
    
    
    def _parseVectorField(self, filename):
        pass
    
    
    def _checkType(self, filename):
        fieldtype = None
        if "scalar" in filename:
            fieldtype = FieldType.SCALAR
        elif "field" in filename:
            fieldtype = FieldType.VECTOR
        
        return fieldtype
    
    
    def getData(self):
        return self._data
