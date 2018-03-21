from visualization.dataset import *
import timing.TimePlot as TimePlot

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
