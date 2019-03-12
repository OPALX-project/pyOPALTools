from opal.datasets.filetype import FileType
from opal.datasets.DatasetBase import DatasetBase
from opal import load_dataset
from opal.analysis.cyclotron import *
import numpy as np
import matplotlib.pyplot as plt
import os

def plot_variability(ds, fname, xvar, yvar, **kwargs):
    """
    Plot the mean, min and max over all samples.
    
    Parameters
    ----------
    ds      (DatasetBase)   datasets
    fname   (str)           file containing the data (xvar and yvar) 
    xvar    (str)           x-axis data
    yvar    (str)           y-axis data
    
    Optional
    --------
    idx     (bool)          fix the x-axis labels (takes the original
                            data order but uses the indices to plot
                            and the values as ticks), useful for
                            periodic values (e.g. azimuth)

    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")

    if not ds.filetype == FileType.SAMPLER:
        raise TypeError(ds.filename + ' is not a sampler dataset.')

    nsamples = ds.size

    dirname = os.path.dirname(ds.filename)
    sdir = os.path.join(dirname, str(0))
    out = load_dataset(sdir, fname=fname)[0]
    ydata = np.zeros(out.size, dtype=np.float)
    ymin  = np.finfo(np.float).max + np.zeros(out.size, dtype=np.float)
    ymax  = np.finfo(np.float).min + np.zeros(out.size, dtype=np.float)

    xdata = out.getData(xvar)

    for i in range(nsamples):
        # load simulation directory
        sdir = os.path.join(dirname, str(i))
        out = load_dataset(sdir, fname=fname)[0]
        data = out.getData(yvar)
        if sort:
            data = data[ind]
        ydata += data
        ymin = np.minimum(ymin, data)
        ymax = np.maximum(ymax, data)

    mean = np.zeros(len(ydata), dtype=np.float)
    mean = ydata / np.float(nsamples)

    if not kwargs.pop('idx', False):
        plt.plot(xdata, mean, **kwargs, color='black', linestyle='dashed', label='mean')
        plt.fill_between(xdata, ymin, ymax,
                         facecolor='blue', alpha=0.2, label='variability region')
    else:
        l = len(xdata)
        ind = np.linspace(0, l-1, l, dtype=int)
        plt.plot(ind, mean, **kwargs, color='black', linestyle='dashed', label='mean')
        plt.fill_between(ind, ymin, ymax,
                         facecolor='blue', alpha=0.2, label='variability region')
        nticks=len(plt.gca().get_xticklabels())
        plt.xticks(xdata)
        # 12. March 2019
        # https://stackoverflow.com/questions/6682784/reducing-number-of-plot-ticks
        plt.locator_params(nbins=nticks)
        
    
    
    plt.legend()

    xlabel = out.getLabel(xvar)
    xunit  = out.getUnit(xvar)

    ylabel = out.getLabel(yvar)
    yunit  = out.getUnit(yvar)

    plt.xlabel(xlabel + ' [' + xunit + ']')
    plt.ylabel(ylabel + ' [' + yunit + ']')

    return plt
