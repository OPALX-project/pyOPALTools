# Author:   Matthias Frey,
#           Philippe Ganz
# Date:     March 2018

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.stats import gaussian_kde
import numpy as np
from opal.datasets.DatasetBase import FileType, DatasetBase
from utilities.LatticeParser import LatticeParser
import os

from opal.visualization.timing.plots import *
from opal.visualization.profiling.memory_plots import *
from opal.visualization.profiling.lbal_plots import *
from opal.visualization.grids.plots import *
from opal.visualization.solver.plots import *


def plot_orbits(ds, **kwargs):
    
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.TRACK_ORBIT:
        raise TypeError(ds.filename + ' is not a track orbit dataset.')
    
    pid = kwargs.get('id', 0)
    
    xdata = ds.getData('x')
    ydata = ds.getData('y')
    ids   = ds.getData('ID')
        
    xdata = xdata[np.where(ids == pid)]
    ydata = ydata[np.where(ids == pid)]
        
    plt.plot(xdata, ydata)
        
    xlabel = ds.getLabel('x')
    xunit  = ds.getUnit('x')
    
    ylabel = ds.getLabel('y')
    yunit  = ds.getUnit('y')
    
    plt.xlabel(xlabel + ' [' + xunit + ']')
    plt.ylabel(ylabel + ' [' + yunit + ']')
    
    return plt


def plot_profile1D(ds, xvar, yvar, **kwargs):
    """
    Plot a 1D profile.
    
    Parameters
    ----------
    ds      (DatasetBase)   datasets
    xvar    (str)           variable for x-axis
    yvar    (str)           variable for y-axis
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    plt.figure()
    plt.xscale(kwargs.get('yscale', 'linear'))
    plt.yscale(kwargs.get('xscale', 'linear'))
    
    if kwargs.get('xsci', False):
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0,3))
    
    if kwargs.get('ysci', False):
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,3))
    
    xdata = ds.getData(xvar)
    ydata = ds.getData(yvar)
    plt.plot(xdata, ydata)
    
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
    bins    (list or integer)   color energy bins
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    step = kwargs.get('step', 0)
    bins = kwargs.get('bins', [])
    
    if not ds.filetype == FileType.H5:
        raise TypeError("Dataset '" + ds.filename + "' is not a H5 file.")
    
    plt.figure()
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
        colors = np.linspace(0, 1, nBins)
        
        for i, b in enumerate(bins):
            xbin = xdata[np.where(bdata == b)]
            ybin = ydata[np.where(bdata == b)]
            plt.scatter(xbin, ybin, marker='.', s=1, c=cm.tab20(colors[i]))
        # plot all skipped bins with same color
        for s in skipped:
            xbin = xdata[np.where(bdata == s)]
            ybin = ydata[np.where(bdata == s)]
            plt.scatter(xbin, ybin, marker='.', s=1, c=cm.tab20(colors[nBins]))
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
    
    22. March 2018
    https://stackoverflow.com/questions/20105364/how-can-i-make-a-scatter-plot-colored-by-density-in-matplotlib
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    xdata = ds.getData(xvar)
    ydata = ds.getData(yvar)
        
    xy = np.vstack([xdata, ydata])
    z = gaussian_kde(xy)(xy)
    plt.scatter(xdata, ydata, c=z, marker='.', s=1)
    
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
    yvars   ([])            list of variables for y-axis
                            (2 entries expected)
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
