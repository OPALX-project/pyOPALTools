# Author:   Matthias Frey
# Date:     April 2018

import matplotlib.pyplot as plt
from opal.datasets.DatasetBase import FileType, DatasetBase

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
