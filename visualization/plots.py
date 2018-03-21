from visualization.dataset import *
import timing.TimePlot as TimePlot
import matplotlib.pyplot as plt

def plot_time(ds, kind='pie', **kwargs):
    """
    
    Parameters
    ----------
    ds      dataset
    kind    of plot
    
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
        for i in range(ds.size):
            files.append(ds.filename(i))
        return tp.automatic(kind, fname=files, **kwargs)
    else:
        for i in range(ds.size):
            return tp.automatic(kind=kind,
                                fname=ds.filename(i), **kwargs)


def plot_profile1D(ds, xvar, yvar, **kwargs):
    
    figsize = kwargs.get('figsize', (7, 7))
    dpi     = kwargs.get('dpi', 300)
    
    plt.figure(figsize=figsize, dpi=dpi)
    plt.xscale(kwargs.get('yscale', 'linear'))
    plt.yscale(kwargs.get('xscale', 'linear'))
    
    if kwargs.get('xsci', False):
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0,3))
    
    if kwargs.get('ysci', False):
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,3))
    
    variables = {'xvar': xvar, 'yvar': yvar}
    
    for i in range(ds.size):
        xdata, ydata, _ = ds.getData(i, **variables)
        xunit, yunit, _ = ds.getUnit(i, **variables)
        plt.plot(xdata, ydata)
    
    plt.xlabel(xvar.lower() + ' [' + xunit + ']')
    plt.ylabel(yvar.lower() + ' [' + yunit + ']')
    
    return plt


def plot_phase_space(ds, xvar, yvar, **kwargs):
    
    if not ds.filetype == FileType.H5:
        raise RuntimeError('Not a H5 dataset.')
    
    figsize = kwargs.get('figsize', (7, 7))
    dpi     = kwargs.get('dpi', 300)
    
    plt.figure(figsize=figsize, dpi=dpi)
    plt.xscale(kwargs.get('yscale', 'linear'))
    plt.yscale(kwargs.get('xscale', 'linear'))
    
    if kwargs.get('xsci', False):
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0,3))
    
    if kwargs.get('ysci', False):
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,3))
    
    variables = {'xvar': xvar, 'yvar': yvar}
    
    for i in range(ds.size):
        xdata, ydata, _ = ds.getData(i, **variables)
        xunit, yunit, _ = ds.getUnit(i, **variables)
        plt.plot(xdata, ydata, '.')
    
    plt.xlabel(xvar.lower() + r' $ [' + xunit + ']$')
    plt.ylabel(yvar.lower() + r' $ [' + yunit + ']$')
    
    plt.tight_layout()
    
    return plt
