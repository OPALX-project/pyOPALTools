import timing.TimePlot as TimePlot
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import numpy as np
from opal.datasets.DatasetBase import FileType
from utilities.LatticeParser import LatticeParser

def plot_time(dsets, kind='pie', **kwargs):
    """
    Do timing plots.
    
    Parameters
    ----------
    dsets   (list)  datasets
    kind    (str)   of plot
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    
    
    if not dsets[0].filetype == FileType.TIMING:
        raise RuntimeError('Not a timing dataset.')
    
    tp = TimePlot()
    
    # treat special case
    if kind == 'line':
        files = []
        for ds in dsets:
            files.append(ds.filename)
        return tp.automatic(kind, fname=files, **kwargs)
    else:
        for ds in dsets:
            return tp.automatic(kind=kind,
                                fname=ds.filename, **kwargs)


def plot_profile1D(dsets, xvar, yvar, **kwargs):
    """
    Plot a 1D profile.
    
    Parameters
    ----------
    dsets   (list)  datasets
    xvar    (str)   variable for x-axis
    yvar    (str)   variable for y-axis
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    plt.figure()
    plt.xscale(kwargs.get('yscale', 'linear'))
    plt.yscale(kwargs.get('xscale', 'linear'))
    
    if kwargs.get('xsci', False):
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0,3))
    
    if kwargs.get('ysci', False):
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,3))
    
    for ds in dsets:
        xdata = ds.getData(xvar)
        ydata = ds.getData(yvar)
        plt.plot(xdata, ydata)
    
    xunit  = dsets[0].getUnit(xvar)
    yunit  = dsets[0].getUnit(yvar)
    xlabel = dsets[0].getLabel(xvar)
    ylabel = dsets[0].getLabel(yvar)
    
    plt.xlabel(xlabel + ' [' + xunit + ']')
    plt.ylabel(ylabel + ' [' + yunit + ']')
    
    return plt


def plot_phase_space(dsets, xvar, yvar, **kwargs):
    """
    Plot a 2D phase space plot.
    
    Parameters
    ----------
    dsets   (list)  datasets
    xvar    (str)   variable for x-axis
    yvar    (str)   variable for y-axis
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    
    for ds in dsets:
        if not ds.filetype == FileType.H5:
            raise RuntimeError("Dataset '" + ds.filename + "' is not a H5 file.")
    
    plt.figure()
    plt.xscale(kwargs.get('yscale', 'linear'))
    plt.yscale(kwargs.get('xscale', 'linear'))
    
    if kwargs.get('xsci', False):
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0,3))
    
    if kwargs.get('ysci', False):
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,3))
    
    for ds in dsets:
        xdata = ds.getData(xvar)
        ydata = ds.getData(yvar)
        plt.scatter(xdata, ydata, marker='.', s=1)
    
    
    xunit  = dsets[0].getUnit(xvar)
    yunit  = dsets[0].getUnit(yvar)
    xlabel = dsets[0].getLabel(xvar)
    ylabel = dsets[0].getLabel(yvar)
    
    plt.xlabel(xlabel + ' [' + xunit + ']')
    plt.ylabel(ylabel + ' [' + yunit + ']')
    
    plt.tight_layout()
    
    return plt


def plot_density(dsets, xvar, yvar, **kwargs):
    """
    
    22. March 2018
    https://stackoverflow.com/questions/20105364/how-can-i-make-a-scatter-plot-colored-by-density-in-matplotlib
    """
    
    for ds in dsets:
        
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


def plot_envelope(dsets, **kwargs):
    """
    Create an envelope plot.
    
    # TODO Philippe
    
    Parameters
    ----------
    dsets   (list)  datasets
    lfile   (str)   lattice file (*.lattice) (optional)
    """
    
    lfile = kwargs.get('lfile', '')
    
    if lfile:
        # call lattice parser to get elements
        pass
    
    plt.figure()
    
    
    
    return plt
