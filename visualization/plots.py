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
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    yscale  = kwargs.get('yscale', 'linear')
    xscale  = kwargs.get('xscale', 'linear')
    
    
    ax.set_xscale(xscale)
    ax.set_yscale(yscale)
    
    variables = {'xvar': xvar, 'yvar': yvar}
    
    for i in range(ds.size):
        xdata, ydata, _ = ds.getData(i, **variables)
        xunit, yunit, _ = ds.getUnit(i, **variables)
        
        ax.plot(xdata, ydata)
    
    ax.set_xlabel(xvar + ' [' + xunit + ']')
    ax.set_ylabel(yvar + ' [' + yunit + ']')
    
    return plt

