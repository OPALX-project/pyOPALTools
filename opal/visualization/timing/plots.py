from opal.datasets.DatasetBase import FileType
import timing.TimePlot as TimePlot
import matplotlib.pyplot as plt

def plot_time(ds, kind='pie', **kwargs):
    """
    Do timing plots.
    
    Parameters
    ----------
    ds      (DatasetBase)   dataset
    kind    (str)           of plot
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    
    
    if not ds.filetype == FileType.TIMING:
        raise RuntimeError('Not a timing dataset.')
    
    tp = TimePlot()
    
    # treat special case
    if kind == 'line':
        if len(ds) < 2:
            raise RuntimeError('More than one dataset required for this plot.')
        files = []
        for d in ds:
            files.append(d.filename)
        return tp.automatic(kind, fname=files, **kwargs)
    else:
        return tp.automatic(kind=kind,
                            fname=ds.filename, **kwargs)
