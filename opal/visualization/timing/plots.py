from opal.datasets.DatasetBase import FileType
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
    
    
    if not dsets[0].filetype == FileType.TIMING:
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
