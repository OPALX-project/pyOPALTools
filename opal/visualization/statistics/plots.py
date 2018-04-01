# Author:   Matthias Frey
# Date:     April 2018

import matplotlib.pyplot as plt
from opal.datasets.DatasetBase import FileType, DatasetBase
from opal.visualization.statistics import impl_plots

def plot_histogram(ds, var, **kwargs):
    """
    Plot a 1D histogram.
    
    Parameters
    ----------
    ds      (DatasetBase)       dataset
    var     (str)               variable to consider
    
    Optional parameters
    -------------------
    step    (int)           of dataset
    bins    (int /str)      binning type or #bins
                            (see https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.histogram.html)
    density (bool)          normalize such that integral over
                            range is 1.
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    step    = kwargs.get('step', 0)
    bins    = kwargs.get('bins', 'sturges')
    density = kwargs.get('density', True)
    
    data = ds.getData(var, step=step)
    
    plt.hist(data, bins=bins, density=density)
    
    xunit  = ds.getUnit(var)
    xlabel = ds.getLabel(var)
    
    plt.xlabel(xlabel + ' [' + xunit + ']')
    
    ylabel = '#entries'
    
    if density:
        ylabel += ' (normalized)'
    plt.ylabel(ylabel)
    
    return plt


def plot_classification(ds, xvar, yvar, value, **kwargs):
    """
    Scatter plot where the points are colored according
    the value of the probability density function
    pdf(x, y) computed through kernel density estimation.
    
    Parameters
    ----------
    ds      (DatasetBase)       dataset
    xvar    (str)               x-axis variable to consider
    yvar    (str)               y-axis variable to consider
    value   (float)             boundary value of classification
    
    Optional parameters
    -------------------
    step    (int)           of dataset
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    step    = kwargs.get('step', 0)
    
    xdata = ds.getData(xvar, step=step)
    ydata = ds.getData(yvar, step=step)
    
    xunit  = ds.getUnit(xvar)
    xlabel = ds.getLabel(xvar)
    
    yunit  = ds.getUnit(yvar)
    ylabel = ds.getLabel(yvar)
    
    plt = impl_plots.plot_classification(xdata, xlabel,
                                         ydata, ylabel,
                                         value)
    
    plt.xlabel(xlabel + ' [' + xunit + ']')
    plt.ylabel(ylabel + ' [' + yunit + ']')
    
    return plt


def plot_joint(ds, xvar, yvar, join, **kwargs):
    """
    
    Parameters
    ----------
    ds      (DatasetBase)       dataset
    xvar    (str)               x-axis variable to consider
    yvar    (str)               y-axis variable to consider
    join    (str)               'all', 'contour' or 'scatter'
    
    Optional parameters
    -------------------
    step        (int)           of dataset
    see also                    help(impl_plots.plot_joint)
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    step    = kwargs.get('step', 0)
    
    xdata = ds.getData(xvar, step=step)
    ydata = ds.getData(yvar, step=step)
    
    xunit  = ds.getUnit(xvar)
    xlabel = ds.getLabel(xvar)
    
    yunit  = ds.getUnit(yvar)
    ylabel = ds.getLabel(yvar)
    
    plt = impl_plots.plot_joint(xdata, xlabel + ' [' + xunit + ']',
                                ydata, ylabel + ' [' + yunit + ']',
                                join, **kwargs)
    
    return plt
