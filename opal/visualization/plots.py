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

from . import  helper

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
    ax      (matplotlib.axes.Axes)     axes object for plotting
    xscale  (str)                      'linear', 'log'
    yscale  (str)                      'linear', 'log'
    xsci    (bool)                     x-ticks in scientific notation
    ysci    (bool)                     y-ticks in scientific notation
    
    Returns
    -------
    a matplotlib.axes.Axes object
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    ax = helper.get_axes(kwargs.pop('axes',''))

    #plt.figure()
    ax.set_xscale(kwargs.pop('yscale', 'linear'))
    ax.set_yscale(kwargs.pop('xscale', 'linear'))
    
    if kwargs.pop('xsci', False):
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0,3))
    
    if kwargs.pop('ysci', False):
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0,3))
    
    xdata = ds.getData(xvar)
    ydata = ds.getData(yvar)
    ax.plot(xdata, ydata, **kwargs)
    
    xunit  = ds.getUnit(xvar)
    yunit  = ds.getUnit(yvar)
    xlabel = ds.getLabel(xvar)
    ylabel = ds.getLabel(yvar)
    
    ax.set_xlabel(xlabel + ' [' + xunit + ']')
    ax.set_ylabel(ylabel + ' [' + yunit + ']')
    
    return ax


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
    ax      (matplotlib.axes.Axes)     axes object for plotting
    step    (int)                      of dataset
    bins    (list or integer)          color energy bins
    xscale  (str)                      'linear', 'log'
    yscale  (str)                      'linear', 'log'
    xsci    (bool)                     x-ticks in scientific notation
    ysci    (bool)                     y-ticks in scientific notation
    
    Returns
    -------
    a matplotlib.axes.Axes object
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
        
    ax = helper.get_axes(kwargs.pop('axes',''))

    step = kwargs.get('step', 0)
    bins = kwargs.get('bins', [])
    
    if not ds.filetype == FileType.H5:
        raise TypeError("Dataset '" + ds.filename + "' is not a H5 file.")
    
    ax.set_xscale(kwargs.get('yscale', 'linear'))
    ax.set_yscale(kwargs.get('xscale', 'linear'))
    
    if kwargs.get('xsci', False):
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0,3))
    
    if kwargs.get('ysci', False):
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0,3))
    
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
            ax.scatter(xbin, ybin, marker='.', s=1, c=cm.tab20(colors[i]))
        # plot all skipped bins with same color
        for s in skipped:
            xbin = xdata[np.where(bdata == s)]
            ybin = ydata[np.where(bdata == s)]
            ax.scatter(xbin, ybin, marker='.', s=1, c=cm.tab20(colors[nBins]))
    else:
        ax.scatter(xdata, ydata, marker='.', s=1)
    
    xunit  = ds.getUnit(xvar)
    yunit  = ds.getUnit(yvar)
    xlabel = ds.getLabel(xvar)
    ylabel = ds.getLabel(yvar)
    
    ax.set_xlabel(xlabel + ' [' + xunit + ']')
    ax.set_ylabel(ylabel + ' [' + yunit + ']')
    
    return ax


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
    ax      (matplotlib.axes.Axes)    axes object for plotting
    step    (int)                     of dataset
    bins    (list, array or integer)  number of bins
    cmap    (Colormap, string)        color map
    levels  (int)                     number of contour levels
   
    Reference (22. March 2018)
    ---------
    https://stackoverflow.com/questions/20105364/how-can-i-make-a-scatter-plot-colored-by-density-in-matplotlib
    
    Returns
    -------
    a matplotlib.axes.Axes object
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    ax = helper.get_axes(kwargs.pop('axes',''))

    step = kwargs.get('step', 0)
    bins = kwargs.get('bins', (50,50))
    cmap = kwargs.get('cmap', plt.cm.jet)
    lvls = kwargs.get('levels',50)
    
    xdata = ds.getData(xvar, step=step)
    ydata = ds.getData(yvar, step=step)
    
    xy = np.vstack([xdata, ydata])
    H,x_edges,y_edges = np.histogram2d(xdata, ydata, bins = bins)
    x_centers = (x_edges[:-1] + x_edges[1:]) / 2
    y_centers = (y_edges[:-1] + y_edges[1:]) / 2
    XX,YY = np.meshgrid(x_centers,y_centers)

    l = np.linspace(np.min(H),np.max(H),lvls)

    ax.contourf(XX,YY,H,levels=l,cmap=cmap)

    xunit  = ds.getUnit(xvar)
    yunit  = ds.getUnit(yvar)
    xlabel = ds.getLabel(xvar)
    ylabel = ds.getLabel(yvar)
    
    ax.set_xlabel(xlabel + ' [' + xunit + ']')
    ax.set_ylabel(ylabel + ' [' + yunit + ']')
    
    return ax
