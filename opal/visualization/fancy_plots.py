# Author:   Ryan Roussel
# Date:     May 2018

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
    a matplotlib.figure.Figure object
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
    return fig
