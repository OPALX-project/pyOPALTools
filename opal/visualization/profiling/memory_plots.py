# Author: Matthias Frey
# Date:   March 2018

from opal.datasets.filetype import FileType
from opal.datasets.DatasetBase import DatasetBase
import matplotlib.pyplot as plt
import numpy as np
import warnings

def plot_total_memory(ds, **kwargs):
    """
    Plot the total memory consumption vs. simulation time.
    
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.MEM:
        raise TypeError(ds.filename + ' is not a memory dataset.')
    
    grid     = kwargs.get('grid', False)
    title    = kwargs.get('title', None)
    yscale   = kwargs.get('yscale', 'linear')
    xscale   = kwargs.get('xscale', 'linear')
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    memory_usage = ds.getData('memory')
    time = ds.getData('t')
    plt.plot(time, memory_usage)
    
    ax.grid(grid, which='both')
    
    memory_unit = ds.getUnit('memory')
    time_unit = ds.getUnit('t')
    
    plt.xlabel('time [' + time_unit + ']')
    plt.xscale(xscale)
    
    plt.ylabel('total memory [' + memory_unit + ']')
    plt.yscale(yscale)
    
    if title:
        plt.title(title)
    
    plt.tight_layout()
    
    return plt


def plot_memory_summary(ds, **kwargs):
    """
    Plot the maximum, minimum and average memory consumption
    vs. simulation time.
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.MEM:
        raise TypeError(ds.filename + ' is not a memory dataset.')
    
    grid     = kwargs.get('grid', False)
    title    = kwargs.get('title', None)
    yscale   = kwargs.get('yscale', 'linear')
    xscale   = kwargs.get('xscale', 'linear')
        
    nTotal = len(ds.getVariables())
    nCols = sum('processor' in var for var in ds.getVariables())
        
    
    time_unit = ds.getUnit('t')
    time = ds.getData('t')
    
    memory_unit = ds.getUnit('memory')
    
    nRows = len(time)
    
    # iterate through all steps and do a boxplot
    colStart = nTotal - nCols
    colEnd   = nCols + 1
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    # each row is a time stamp
    minimum = []
    maximum = []
    mean    = []
    for r in range(0, nRows):
        stamp = np.empty([nCols,], dtype=float)
        for c in range(colStart, colEnd+1):
            cc = c - colStart
            stamp[cc] = float(ds.getData('processor-' + str(cc))[r])
        minimum.append(min(stamp))
        mean.append(np.mean(stamp))
        maximum.append(max(stamp))
    
    plt.plot(time, minimum, label='minimum')
    plt.plot(time, maximum, label='maximum')
    plt.plot(time, mean, label='mean')
    
    plt.xlabel('time [' + time_unit + ']')
    plt.xscale(xscale)
        
    plt.ylabel('memory [' + memory_unit + ']')
    plt.yscale(yscale)
    
    plt.legend()
    
    plt.grid(grid, which='both')
    
    if title:
        plt.title(title)
    
    plt.tight_layout()
    
    return plt


def plot_memory_boxplot(ds, **kwargs):
    
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.MEM:
        raise TypeError(ds.filename + ' is not a memory dataset.')
    
    grid     = kwargs.get('grid', False)
    title    = kwargs.get('title', None)
    yscale   = kwargs.get('yscale', 'linear')
    xscale   = kwargs.get('xscale', 'linear')
    
    nTotal = len(ds.getVariables())
    nCols = sum('processor' in var for var in ds.getVariables())
    
    time_unit = ds.getUnit('t')
    time = ds.getData('t')
    
    memory_unit = ds.getUnit('memory')
    
    nRows = len(time)
    
    # iterate through all steps and do a boxplot
    colStart = nTotal - nCols
    colEnd   = nCols + 1
    
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
    
    # each row is a time stamp
    stamps = []
    for r in range(0, nRows):
        stamp = np.empty([nCols,], dtype=float)
        for c in range(colStart, colEnd+1):
            cc = c - colStart
            stamp[cc] = float(ds.getData('processor-' + str(cc))[r])
        stamps.append(stamp)
    
    if xscale == 'log':
        # 24. Dec. 2017
        # https://stackoverflow.com/questions/19328537/check-array-for-values-equal-or-very-close-to-zero
        # https://stackoverflow.com/questions/19141432/python-numpy-machine-epsilon
        if np.any(np.absolute(time) < np.finfo(float).eps):
            warnings.warn('Entry close to zero. Switching to linear x scale',
                            RuntimeWarning)
            xscale='linear'
    
    plt.boxplot(stamps, 0, '', positions=time)
    
    plt.xlabel('time [' + time_unit + ']')
    plt.xscale(xscale)
    
    plt.ylabel('memory [' + memory_unit + ']')
    plt.yscale(yscale)
    
    plt.grid(grid, which='both')
    
    if title:
        plt.title(title)
    
    plt.tight_layout()
    
    return plt
