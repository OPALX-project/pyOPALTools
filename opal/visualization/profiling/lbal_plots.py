# Author: Matthias Frey
# Date:   December 2017 - March 2018

from opal.datasets.filetype import FileType
from opal.datasets.DatasetBase import DatasetBase
import matplotlib.pyplot as plt
import numpy as np
import warnings

def plot_lbal_histogram(ds, **kwargs):
    """
    Particle load balancing.
    
    Plots the time series (i.e. simulation time) histogram with
    the number of cores having the same amount of particles.
    The user can specify ranges givin the upper and lower
    boundary, i.e. 'bupper' and, respectively, 'blower'. Those
    boundaries are given in percent.
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.LBAL:
        raise TypeError(ds.filename + ' is not a load balancing dataset.')
    
    grid     = kwargs.pop('grid', False)
    title    = kwargs.pop('title', None)
    yscale   = kwargs.pop('yscale', 'linear')
    xscale   = kwargs.pop('xscale', 'linear')
    blower   = kwargs.pop('blower', [0.0, 0.0,  25.0, 50.0, 75.0])
    bupper   = kwargs.pop('bupper', [0.0, 25.0, 50.0, 75.0, 100.0])
    
    if not len(blower) == len(bupper):
        raise ValueError('len(blower) != len(bupper)')
        
    nTotal = len(ds.getVariables())
    nCols = sum('processor' in var for var in ds.getVariables())
    
    time_unit = ds.getUnit('time')
    time = ds.getData('time')
    
    nRows = len(time)
    
    # iterate through all steps and do a boxplot
    colStart = nTotal - nCols
    colEnd   = nCols + 1
    
    # percentages with respect to expected average number p / t
    # where p is the number of particles per processes and t the total
    # number of particles
    stamps = np.empty([nRows, len(blower)], dtype=float)
    
    p = 100.0 / nCols   # in percent [%]
        
    # each row is a time stamp
    for r in range(0, nRows):
        stamp = np.empty([nCols,], dtype=float)
        for c in range(colStart, colEnd):
            cc = c - colStart
            stamp[cc] = float(ds.getData('processor-' + str(cc))[r])
        # total number of particles
        total = sum(stamp)
        
        # percentage []
        stamp /= total * 0.01 # in %
        
        # check bin
        for i in range(0, len(blower)):
            
            if blower[i] == bupper[i]:
                stamps[r, i] = ((blower[i] <= stamp) & (stamp <= bupper[i])).sum()
            else:
                stamps[r, i] = ((blower[i] < stamp) & (stamp <= bupper[i])).sum()
    
    for i in range(0, len(blower)):
    
        common = str(blower[i]) + ', ' + str(bupper[i]) + '] %'
        lab = ']' + common
            
        if blower[i] == bupper[i]:
            lab = '[' + common
            
        plt.plot(time, stamps[:, i], label=lab)
    
    
    xlabel = ds.getLabel('time')
    plt.xlabel(xlabel + ' [' + time_unit + ']')
    plt.xscale(xscale)
    
    plt.ylabel('#cores')
    plt.yscale(yscale)
    
    plt.legend()
    
    plt.grid(grid, which='both')
    
    if title:
        plt.title(title)
    
    plt.tight_layout()
    
    return plt


def plot_lbal_summary(ds, **kwargs):
    """
    Particle load balancing.
    
    Plot the minimum, maximum and average number of
    particles per core vs. the simulation time.
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.LBAL:
        raise TypeError(ds.filename + ' is not a load balancing dataset.')
    
    grid     = kwargs.pop('grid', False)
    title    = kwargs.pop('title', None)
    yscale   = kwargs.pop('yscale', 'linear')
    xscale   = kwargs.pop('xscale', 'linear')
    
    nTotal = len(ds.getVariables())
    nCols = sum('processor' in var for var in ds.getVariables())
    
    
    time_unit = ds.getUnit('time')
    time = ds.getData('time')
    
    nRows = len(time)
    
    # iterate through all steps
    colStart = nTotal - nCols
    colEnd   = nCols + 1
    
    # each row is a time stamp
    minimum = []
    maximum = []
    mean    = []
    for r in range(0, nRows):
        stamp = np.empty([nCols,], dtype=float)
        for c in range(colStart, colEnd):
            cc = c - colStart
            stamp[cc] = ds.getData('processor-' + str(cc))[r]
        minimum.append(min(stamp))
        mean.append(np.mean(stamp))
        maximum.append(max(stamp))
    
    plt.plot(time, minimum, label='minimum')
    plt.plot(time, maximum, label='maximum')
    plt.plot(time, mean, label='mean')
    
    xlabel = ds.getLabel('time')
    plt.xlabel(xlabel + ' [' + time_unit + ']')
    plt.xscale(xscale)
    
    plt.ylabel('#particles')
    plt.yscale(yscale)
    
    plt.legend()
    
    plt.grid(grid, which='both')
    
    if title:
        plt.title(title)
    
    plt.tight_layout()
    return plt
    
    
def plot_lbal_boxplot(ds, **kwargs):
    """
    Particle load balancing.
    
    Does a (simulation) time series boxplot of the
    particle load balancing.
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.LBAL:
        raise TypeError(ds.filename + ' is not a load balancing dataset.')
    
    grid     = kwargs.pop('grid', False)
    title    = kwargs.pop('title', None)
    yscale   = kwargs.pop('yscale', 'linear')
    xscale   = kwargs.pop('xscale', 'linear')
    
    nTotal = len(ds.getVariables())
    nCols = sum('processor' in var for var in ds.getVariables())
    
    
    time_unit = ds.getUnit('time')
    time = ds.getData('time')
    
    nRows = len(time)
    
    # iterate through all steps and do a boxplot
    colStart = nTotal - nCols
    colEnd   = nCols + 1
    
    # each row is a time stamp
    stamps = []
    for r in range(0, nRows):
        stamp = np.empty([nCols,], dtype=float)
        for c in range(colStart, colEnd):
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
    
    xlabel = ds.getLabel('time')
    plt.xlabel(xlabel + ' [' + time_unit + ']')
    plt.xscale(xscale)
    
    plt.ylabel('#particles')
    plt.yscale(yscale)
    
    plt.grid(grid, which='both')
    
    if title:
        plt.title(title)
    
    plt.tight_layout()
    
    return plt
