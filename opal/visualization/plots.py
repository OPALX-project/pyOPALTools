# Author:   Matthias Frey,
#           Philippe Ganz
# Date:     March 2018

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.stats import gaussian_kde
import numpy as np
from opal.datasets.filetype import FileType
from opal.datasets.DatasetBase import DatasetBase
from opal.parser.LatticeParser import LatticeParser
import os

from opal.visualization.timing.plots import *
from opal.visualization.profiling.memory_plots import *
from opal.visualization.profiling.lbal_plots import *
from opal.visualization.grids.plots import *
from opal.visualization.solver.plots import *
from opal.visualization.statistics.plots import *
from opal.visualization.cyclotron.plots import *
from opal.visualization.optimizer.plots import *
from opal.visualization.sampler.plots import *


def plot_profile1D(ds, xvar, yvar, **kwargs):
    """
    Plot a 1D profile.
    
    Parameters
    ----------
    ds      (DatasetBase)   datasets
    xvar    (str)           variable for x-axis
    yvar    (str)           variable for y-axis
    
    Optional parameters
    -------------------
    xscale  (str)               'linear', 'log'
    yscale  (str)               'linear', 'log'
    xsci    (bool)              x-ticks in scientific notation
    ysci    (bool)              y-ticks in scientific notation
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    #plt.figure()
    plt.xscale(kwargs.pop('yscale', 'linear'))
    plt.yscale(kwargs.pop('xscale', 'linear'))
    
    if kwargs.pop('xsci', False):
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0,3))
    
    if kwargs.pop('ysci', False):
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,3))
    
    xdata = ds.getData(xvar)
    ydata = ds.getData(yvar)
    plt.plot(xdata, ydata, **kwargs)
    
    xunit  = ds.getUnit(xvar)
    yunit  = ds.getUnit(yvar)
    xlabel = ds.getLabel(xvar)
    ylabel = ds.getLabel(yvar)
    
    plt.xlabel(xlabel + ' [' + xunit + ']')
    plt.ylabel(ylabel + ' [' + yunit + ']')
    
    return plt


def plot_phase_space(ds, xvar, yvar, **kwargs):
    """
    Plot a 2D phase space plot.
    
    Parameters
    ----------
    ds      (DatasetBase)       datasets
    xvar    (str)               variable for x-axis
    yvar    (str)               variable for y-axis
    
    Optional parameters
    -------------------
    step    (int)               of dataset
    bins    (list or integer)   color energy bins
    xscale  (str)               'linear', 'log'
    yscale  (str)               'linear', 'log'
    xsci    (bool)              x-ticks in scientific notation
    ysci    (bool)              y-ticks in scientific notation
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    step    = kwargs.get('step', 0)
    bins    = kwargs.get('bins', [])
    bunches = kwargs.get('bunches', [])
    
    if not ds.filetype == FileType.H5:
        raise TypeError("Dataset '" + ds.filename + "' is not a H5 file.")
    
    plt.xscale(kwargs.get('yscale', 'linear'))
    plt.yscale(kwargs.get('xscale', 'linear'))
    
    if kwargs.get('xsci', False):
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0,3))
    
    if kwargs.get('ysci', False):
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,3))
    
    xdata = ds.getData(xvar, step=step)
    ydata = ds.getData(yvar, step=step)
    
    if bins and ds.filetype == FileType.H5:
        bdata = ds.getData('bin', step=step)
        
        # get all bins not in plotted
        bmin = min(bdata)
        bmax = max(bdata)
        # 27. March 2018
        # https://stackoverflow.com/questions/6486450/python-compute-list-difference
        skipped = set(range(bmin, bmax+1)) - set(bins)
        
        nBins = len(bins) + 1
        colors = np.linspace(0, 1, nBins + 1)
        
        for i, b in enumerate(bins):
            xbin = xdata[np.where(bdata == b)]
            ybin = ydata[np.where(bdata == b)]
            plt.scatter(xbin, ybin, marker='.', s=1, color=cm.tab20(colors[i]))
        # plot all skipped bins with same color
        for s in skipped:
            xbin = xdata[np.where(bdata == s)]
            ybin = ydata[np.where(bdata == s)]
            plt.scatter(xbin, ybin, marker='.', s=1, color=cm.tab20(colors[nBins]))
    elif bunches and ds.filetype == FileType.H5:
        bdata = ds.getData('bunchNumber', step=step)
        # get all bunches
        bmin = min(bdata)
        bmax = max(bdata)
        # 27. March 2018
        # https://stackoverflow.com/questions/6486450/python-compute-list-difference
        skipped = set(range(bmin, bmax+1)) - set(bunches)
        
        nBunches = len(bunches) + 1
        colors = np.linspace(0, 1, nBunches + 1)
        
        # plot all skipped bunches with same color
        for s in skipped:
            xbin = xdata[np.where(bdata == s)]
            ybin = ydata[np.where(bdata == s)]
            plt.scatter(xbin, ybin, marker='.', s=1, color=cm.tab20(colors[nBunches]))
        for i, b in enumerate(bunches):
            xbin = xdata[np.where(bdata == b)]
            ybin = ydata[np.where(bdata == b)]
            plt.scatter(xbin, ybin, marker='.', s=1, color=cm.tab20(colors[i]))
    else:
        plt.scatter(xdata, ydata, marker='.', s=1)
    
    xunit  = ds.getUnit(xvar)
    yunit  = ds.getUnit(yvar)
    xlabel = ds.getLabel(xvar)
    ylabel = ds.getLabel(yvar)
    
    plt.xlabel(xlabel + ' [' + xunit + ']')
    plt.ylabel(ylabel + ' [' + yunit + ']')
    
    plt.tight_layout()
    
    return plt


def plot_density(ds, xvar, yvar, **kwargs):
    """
    Do a density plot.
    
    Parameters
    ----------
    ds      (DatasetBase)       dataset
    xvar    (str)               x-axis variable to consider
    yvar    (str)               y-axis variable to consider
    
    Optional parameters
    -------------------
    step    (int)           of dataset
    bins    (list, array or integer) number of bins
    cmap    (Colormap, string)  color map
   
    Reference (22. March 2018)
    ---------
    https://stackoverflow.com/questions/20105364/how-can-i-make-a-scatter-plot-colored-by-density-in-matplotlib
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    step = kwargs.get('step', 0)
    bins = kwargs.get('bins', (50,50))
    cmap = kwargs.get('cmap', plt.cm.jet)
    
    xdata = ds.getData(xvar, step=step)
    ydata = ds.getData(yvar, step=step)
    
    xy = np.vstack([xdata, ydata])
    plt.hist2d(xdata, ydata, bins = bins, cmap=cmap)

    xunit  = ds.getUnit(xvar)
    yunit  = ds.getUnit(yvar)
    xlabel = ds.getLabel(xvar)
    ylabel = ds.getLabel(yvar)
    
    plt.xlabel(xlabel + ' [' + xunit + ']')
    plt.ylabel(ylabel + ' [' + yunit + ']')
    
    return plt


def plot_envelope(dsets, xvar='position', **kwargs):
    """
    Create an envelope plot.
    
    Parameters
    ----------
    dsets   (DatasetBase)   datasets
    lfile   (str)           lattice file (*.lattice) (optional)
    xvar    (str)           x-axis variable
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not isinstance(dsets, list):
        raise TypeError("Input 'dsets' has to be a list")
    
    if not dsets:
        raise IndexError('Dataset list is empty.')
    
    for ds in dsets:
        if not isinstance(ds, DatasetBase):
            raise TypeError("Dataset '" + ds.filename +
                            "' not derived from 'DatasetBase'.")
    
    ymax = kwargs.get('ymax', 0.03)
    
    lfile = kwargs.get('lfile', '')
    
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, dpi=150)
    fig.set_size_inches(9,4)
    
    if lfile:
        lattice = LatticeParser()
        lattice.plot(lfile, fig, ax1, ax2)
    
    y1label = dsets[0].getLabel('rms_x')
    y2label = dsets[0].getLabel('rms_y')
    
    xunit = dsets[0].getUnit(xvar)
    yunit = dsets[0].getUnit('rms_x')
    
    for ds in dsets:
        xdata =  ds.getData(xvar)
        y1data = ds.getData('rms_x')
        ax1.plot(xdata, y1data, label=os.path.basename(ds.filename))
    
    # 27. March 2018
    # https://stackoverflow.com/questions/20350503/remove-first-and-last-ticks-label-of-each-y-axis-subplot
    plt.setp(ax1.get_yticklabels()[0], visible=False)
    
    ax2 = plt.gca()
    plt.gca().invert_yaxis()
    
    for ds in dsets:
        xdata =  ds.getData(xvar)
        y2data = ds.getData('rms_y')
        ax2.plot(xdata, y2data)
    
    # 27. March 2018
    # https://stackoverflow.com/questions/925024/how-can-i-remove-the-top-and-right-axis-in-matplotlib
    ax1.spines['bottom'].set_visible(False)
    ax1.get_xaxis().set_visible(False)
    
    #for ax in [ax1,ax2]:
    ax2.set_xlabel(xvar + ' [' + xunit + ']')
    
    ax1.set_ylabel(y1label + ' [' + yunit + ']')
    ax2.set_ylabel(y2label + ' [' + yunit + ']')
   
    
    ax1.set_ylim(ymin=0, ymax=ymax)
    ax2.set_ylim(ymax=0, ymin=ymax)
    
    ax1.legend(bbox_to_anchor=(0.6, 1.08))
    
    ax2.xaxis.set_label_position('bottom') 
    ax2.xaxis.set_ticks_position('bottom')
    
    fig.subplots_adjust(hspace = 0.0)
    return plt
