# Author: Matthias Frey
# Date:   February 2018 - March 2019

from opal.visualization.BasePlotter import *
import numpy as np

class SolverPlotter(BasePlotter):
    
    def __init__(self):
        pass
    
    def plot_solver_histogram(self, var, **kwargs):
        """
        Plot a time series of solver output, e.g. error,
        number of iterations, etc.
        """
        hspan  = kwargs.pop('hspan', [None, None])
        grid   = kwargs.pop('grid', False)
        xscale = kwargs.pop('xscale', 'linear')
        yscale = kwargs.pop('yscale', 'linear')
        
        if hspan[0] and hspan[1]:
            plt.axhspan(hspan[0], hspan[1],
                        alpha=0.25, color='purple',
                        label='[' + str(hspan[0]) + ', ' + str(hspan[1]) +']')
            
        time = self.ds.getData('time')
        data = self.ds.getData(var)
        plt.plot(time, data)
        
        plt.xlabel(self.ds.getLabel('time') + ' [' + self.ds.getUnit('time') + ']')
        
        if self.ds.getUnit(var) == r'$1$':
            plt.ylabel(self.ds.getLabel(var))
        else:
            print ( self.ds.getUnit(var) )
            plt.ylabel(self.ds.getLabel(var) + ' [' + self.ds.getUnit(var) + ']')
            
        plt.grid(grid, which='both')
        plt.xscale(xscale)
            plt.yscale(yscale)
        plt.tight_layout()
        plt.legend()
        
        return plt
