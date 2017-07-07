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
    
    
    # 7. July 2017
    # copied from 
    # https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Longest_common_substring#Python_3
    def longest_common_substring(self, s1, s2):
        m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
        longest, x_longest = 0, 0
        for x in range(1, 1 + len(s1)):
            for y in range(1, 1 + len(s2)):
                if s1[x - 1] == s2[y - 1]:
                    m[x][y] = m[x - 1][y - 1] + 1
                    if m[x][y] > longest:
                        longest = m[x][y]
                        x_longest = x
                else:
                    m[x][y] = 0
        return s1[x_longest - longest: x_longest]
