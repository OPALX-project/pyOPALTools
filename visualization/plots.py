from visualization.dataset import *
import timing.TimePlot as TimePlot
import matplotlib.pyplot as plt

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
    
    
    if not ds.filetype == FileType.TIMING:
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
        plt.plot(xdata, ydata, '.')
    
    
    xunit  = dsets[0].getUnit(xvar)
    yunit  = dsets[0].getUnit(yvar)
    xlabel = dsets[0].getLabel(xvar)
    ylabel = dsets[0].getLabel(yvar)
    
    plt.xlabel(xlabel + ' [' + xunit + ']')
    plt.ylabel(ylabel + ' [' + yunit + ']')
    
    plt.tight_layout()
    
    return plt
