from abc import ABC, abstractmethod
import os

class Plotter(ABC):
    
    def __init__(self):
        
        self._parser = []
        self._basenames = []
        self._dirnames = []
        
    
    def addDataset(self, filename, theParser ):
        self._parser.append( theParser )
        self._parser[-1].parse(filename)
        self._basenames.append( os.path.basename(filename) )
        self._dirnames.append( os.path.dirname(filename) )
    
    
    def clear(self):
        self._parser = []
        self._basenames = []
        self._dirnames = []
    
    
    @abstractmethod
    def plot(self, xvar, yvar, canvas):
        print ( "This function should never be executed" )
    
    
    @abstractmethod
    def lineplot(self, canvas):
        print ( "This function should never be executed" )