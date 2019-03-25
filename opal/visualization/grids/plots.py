# Author: Matthias Frey
# Date:   February 2018 - March 2018

from opal.datasets.filetype import FileType
from opal.datasets.DatasetBase import DatasetBase
import matplotlib.pyplot as plt
import numpy as np

def plot_grids_per_level(ds, **kwargs):
    """
    Plot a time series of the number of grids per level
    and the total number of grids.
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.GRID:
        raise TypeError(ds.filename + ' is not a grid dataset.')
    
    hspan  = kwargs.pop('hspan', [None, None])
    grid   = kwargs.pop('grid', False)
    xscale = kwargs.pop('xscale', 'linear')
    yscale = kwargs.pop('yscale', 'linear')
    
    if hspan[0] and hspan[1]:
        plt.axhspan(hspan[0], hspan[1],
                    alpha=0.25, color='purple',
                    label='[' + str(hspan[0]) + ', ' + str(hspan[1]) +']')
    
    nLevels = ds.getNumLevels()
    
    time = ds.getData('time')
    
    total = [0] * len(time)
    for l in range(nLevels):
        level = ds.getData('level-' + str(l))
        plt.plot(time, level, label='level ' + str(l))
        total += level
    
    plt.plot(time, total, label='total')
    plt.xlabel(ds.getLabel('time') + ' [' + ds.getUnit('time') + ']')
    plt.ylabel('#grids')
    plt.xscale(xscale)
    plt.yscale(yscale)
    plt.grid(grid, which='both')
    plt.tight_layout()
    plt.legend()
    
    return plt


def plot_grid_histogram(ds, **kwargs):
    """
    Plot a time series of the minimum, maximum and
    average number of grids per core.
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.GRID:
        raise TypeError(ds.filename + ' is not a grid dataset.')
    
    hspan  = kwargs.pop('hspan', [None, None])
    grid   = kwargs.pop('grid', False)
    xscale = kwargs.pop('xscale', 'linear')
    yscale = kwargs.pop('yscale', 'linear')
    
    nCores= ds.getNumCores()
    
    if hspan[0] and hspan[1]:
        mingrid = hspan[0] / float(nCores)
        maxgrid = hspan[1] / float(nCores)
        # 2. Feb. 2018
        # https://stackoverflow.com/questions/23248435/fill-between-two-vertical-lines-in-matplotlib
        plt.axhspan(mingrid, maxgrid,
                    alpha=0.25, color='purple',
                    label='optimum')
    
    time = ds.getData('time')
    
    low  = np.asarray([np.Inf] * len(time))
    high = np.asarray([-np.Inf] * len(time))
    avg  = np.asarray([0.0] * len(time))
    
    for c in range(nCores):
        data = ds.getData('processor-' + str(c))
        
        low = np.minimum(low, data)
        avg += data
        high = np.maximum(high, data)
        
        #for j in range(len(data)):
        #    low[j] = min(low[j], data[j])
        #    avg[j] = avg[j] + data[j]
        #    high[j] = max(high[j], data[j])
    
    avg /= float(nCores)
    
    plt.plot(time, low, label='minimum')
    plt.plot(time, high, label='maximum')
    plt.plot(time, avg, label='mean')
    
    plt.xscale(xscale)
    plt.yscale(yscale)
    
    plt.xlabel(ds.getLabel('time') + ' [' + ds.getUnit('time') + ']')
    plt.ylabel('#grids per core')
    plt.grid(grid, which='both')
    plt.tight_layout()
    plt.legend()
    
    return plt
