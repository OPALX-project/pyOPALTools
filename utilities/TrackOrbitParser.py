# Author:   Matthias Frey
# Date:     March 2018

class TrackOrbitParser:
    
    def __init__(self):
        self._units = {}
        self._variables = {}
        
    
    def parse(self, filename):
        
        with open(filename) as f:
            for line in f:
                print ( line )
        
    
    
    #def getDataOf