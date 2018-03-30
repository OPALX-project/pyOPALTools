# Author:   Matthias Frey
# Date:     March 2018

from opal.datasets.DatasetBase import FileType, DatasetBase
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
    if kind == 'line':
        if not isinstance(ds, list):
            raise TypeError("Input 'ds' has to be a list for 'line' plot type.")
        if len(ds) < 2:
            raise ValueError("More than one dataset required for 'line' plot.")
        for d in ds:
            if not d.filetype == FileType.TIMING:
                raise TypeError("Dataset '" + d.filename +
                                "' is not a timing dataset.")
    else:
        if not isinstance(ds, DatasetBase):
            raise TypeError("Dataset '" + ds.filename +
                            "' not derived from 'DatasetBase'.")
        if not ds.filetype == FileType.TIMING:
            raise TypeError('Not a timing dataset.')
    
    tp = TimePlot()
    
    # treat special case
    if kind == 'line':
        files = []
        for d in ds:
            files.append(d.filename)
        return tp.automatic(kind, fname=files, **kwargs)
    else:
        return tp.automatic(kind=kind,
                            fname=ds.filename, **kwargs)
