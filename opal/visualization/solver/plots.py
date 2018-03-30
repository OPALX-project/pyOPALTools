# Author: Matthias Frey
# Date:   February 2018 - March 2018

from opal.datasets.DatasetBase import FileType, DatasetBase
import matplotlib.pyplot as plt
import numpy as np

def plot_solver_histogram(ds, var, **kwargs):
    """
    Plot a time series of solver output, e.g. error,
    number of iterations, etc.
    """
    if not isinstance(ds, DatasetBase):
        raise RuntimeError("Dataset '" + ds.filename +
                           "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.SOLVER:
        raise RuntimeError(ds.filename + ' is not a solver dataset.')
    
    hspan  = kwargs.get('hspan', [None, None])
    grid   = kwargs.get('grid', False)
    xscale = kwargs.get('xscale', 'linear')
    yscale = kwargs.get('yscale', 'linear')
    
    plt.figure()
    
    plt.xscale(xscale)
    plt.yscale(yscale)
    
    if hspan[0] and hspan[1]:
        plt.axhspan(hspan[0], hspan[1],
                    alpha=0.25, color='purple',
                    label='[' + str(hspan[0]) + ', ' + str(hspan[1]) +']')
        
    time = ds.getData('time')
    data = ds.getData(var)
    plt.plot(time, data)
    
    plt.xlabel(ds.getLabel('time') + ' [' + ds.getUnit('time') + ']')
    
    if ds.getUnit(var) == r'$1$':
        plt.ylabel(ds.getLabel(var))
    else:
        print ( ds.getUnit(var) )
        plt.ylabel(ds.getLabel(var) + ' [' + ds.getUnit(var) + ']')
        
    plt.grid(grid, which='both')
    plt.tight_layout()
    plt.legend()
    
    return plt
