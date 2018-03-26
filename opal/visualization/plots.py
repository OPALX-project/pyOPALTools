import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import numpy as np
from opal.datasets.DatasetBase import FileType
from utilities.LatticeParser import LatticeParser

from opal.visualization.timing.plots import *
from opal.visualization.profiling.memory_plots import *
from opal.visualization.profiling.lbal_plots import *
from opal.visualization.grids.plots import *
from opal.visualization.solver.plots import *


def plot_orbits(dsets, **kwargs):
    
    for ds in dsets:
        if not ds.filetype == FileType.TRACK_ORBIT:
            raise RuntimeError(ds.filename + ' is not a track orbit dataset.')
    
    pid = kwargs.get('id', 0)
    
    for ds in dsets:
        
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


def plot_envelope(dslist, yvar='rms', xvar='s', **kwargs):
    """
    Create an envelope plot.
    
    # TODO Philippe
    
    Parameters
    ----------
    dsets   (list)  datasets
    lfile   (str)   lattice file (*.lattice) (optional)
    """
    
    lfile = kwargs.get('lfile', '')
    
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, dpi=150)
    fig.set_size_inches(9,4)
     
    if lfile:
        Lattice=LatticeParser()
        Lattice.plotLattice(lfile, fig, ax1, ax2)
    
    yvarvec=[yvar+"_x", yvar+"_y"]
    

    for dsets in dslist:
        for ds in dsets:
            print(ds)
            xdata =  ds.getData(xvar)
            y1data = ds.getData(yvarvec[1])
            y2data = ds.getData(yvarvec[0])
            
            xunit=ds.getUnit(xvar)
            yunit=ds.getUnit(yvarvec[0])
            
            ax1.plot(xdata, y1data,label=' [' + yunit + ']')
            ax2.plot(xdata, y2data)
    
    for ax in [ax1,ax2]:
        ax.set_xlabel(xvar + ' [' + xunit + ']')
        
    ax1.set_ylabel(yvar+"_x" + ' [' + yunit + ']')
    ax2.set_ylabel(yvar+"_y" + ' [' + yunit + ']')
   
    ax2 = plt.gca()
    plt.gca().invert_yaxis()
           
        
    ax1.set_ylim(ymin=0,ymax=0.03)
    ax2.set_ylim(ymax=0,ymin=0.03)
    
    ax2.xaxis.set_label_position('top') 
    ax2.xaxis.set_ticks_position('top')
    
    fig.subplots_adjust(hspace = .001)
    fig.suptitle('Comparison OPAL Algorithms')
    fig.legend(loc=4)
    
    plt.figure()
    
    return plt
