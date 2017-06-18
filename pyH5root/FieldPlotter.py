from Plotter import *
import FieldParser as fieldparser
import numpy as np

class FieldPlotter(Plotter):
    
    def __init__(self):
        super(FieldPlotter, self).__init__()
        
    def plot(self, xvar, yvar, canvas):
        raise RuntimeError("Not implemented.")
    
    def lineplot(self, canvas):
        # obtain the maximum value for each z-layer
        
        axes = canvas.getAxes()
        
        for i in range(0, len( self._parser )):
            values = np.array([])
            data = self._parser[i].getData()
            
            z = data[:, 2]
            value = data[:, 3]
            
            n = int(max(z))
            
            for j in range(0, n-1):
                tmp = np.extract(z == j+1, value)
                pmax = max(tmp)
                values = np.append(values, [pmax])
        
            canvas.addLegend(self._basenames[i])
            axes.plot(values)
        
        axes.set_xlabel('z')
        axes.set_ylabel('max. value')
        axes.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
