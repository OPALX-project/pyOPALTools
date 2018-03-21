from utilities.H5Parser import H5Parser

class H5Dataset:
    
    def __init__(self, directory, fname):
        self.__directory = directory
        self.__fname = fname
        
        self.__parser = H5Parser()
        self.__parser.parse(directory + fname)
    
    
    def getData(self, var, step):
        """
        Automatic selection of data.
        """
        if var in self.__parser.getStepDatasets(step):
            return self.__parser.getStepDataset(var, step)
        elif var in self.__parser.getStepAttributes(step):
            data = []
            for i in range(self.__parser.getNSteps()):
                data.append(self.__parser.getStepAttribute(var, i))
            return data
        else:
            raise H5Error("'" + var + "' is not part of this step")
    
    
    def getUnit(self, var):
        """
        Automatic selection of unit of data.
        """
        
        unit = self.__parser.getGlobalAttribute(var + 'Unit')
        return unit.replace('#', '\\')
