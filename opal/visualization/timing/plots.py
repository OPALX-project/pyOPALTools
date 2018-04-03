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


def plot_efficiency(dsets, what, prop, **kwargs):
    """
    Efficiency plot of a timing benchmark study
    
    E_p = S_p / p
    
    where E_p is the efficiency and S_p the
    speed-up with p cores / nodes.
    
    Parameters
    ----------
    dsets   ([DatasetBase]) all timing datasets
    what    (str)           timing name
    prop    (str)           property, i.e. 'cpu avg', 'cpu max', 'cpu min',
                            'wall avg', 'wall max', 'wall min' or
                            'cpu tot' and 'wall tot' (only for main timing)
    
    Optionals
    ---------
    xscale  (str)           x-axis scale, 'linear' or 'log'
    yscale  (str)           y-axis scale, 'linear' or 'log'
    grid    (bool)          if true, plot grid
    percent (bool)          efficiency in percentage
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not isinstance(dsets, list):
        raise TypeError("Input 'dsets' has to be a list for.")
    
    if not dsets:
        raise ValueError("No dataset in 'dsets'.")
    
    for ds in dsets:
        if not isinstance(ds, DatasetBase):
            raise TypeError("Dataset '" + ds.filename +
                            "' not derived from 'DatasetBase'.")
        if not ds.filetype == FileType.TIMING and not ds.filetype == FileType.OUTPUT:
            raise TypeError("Dataset '" + ds.filename +
                            "' is not a timing dataset.")
    
    cores = []

    # find timing dictionary of corresponding property 'prop'
    # 'idx' will be set accordingly
    idx = 0
    match = False
    available = []
    for timing in dsets[0].getData(''):
        if timing['what'] == what:
            match = True
        else:
            available.append( timing['what'] )
            idx += 1
    
    if not match:
        raise ValueError("No timing called '" + what + "'. Possible entries:"
                         + str(available))
    
    # clear again
    available = []
    
    time = []
    
    for ds in dsets:
        data = ds.getData('')
        
        #access main timing
        cores.append( int(data[0]['cores']) )
        
        time.append( data[idx][prop] )
    
    # sort
    cores, time = zip(*sorted(zip(cores, time)))
    
    
    # obtain speed-up
    speedup = []
    for t in time:
        speedup.append( time[0] / t )
    
    # obtain core increase
    incr = []
    for c in cores:
        incr.append( c / cores[0] )   
    
    # obtain efficiency
    efficiency = []
    
    percent = 1.0
    ylabel  = 'efficiency'
    if kwargs.get('percent', True):
        percent = 100.0
        ylabel += ' [%]'
    
    for i, s in enumerate(speedup):
        efficiency.append( s / incr[i] * percent ) # in percent
    
    xscale = kwargs.get('xscale', 'linear')
    yscale = kwargs.get('yscale', 'linear')
    grid   = kwargs.get('grid', False)
    
    plt.plot(cores, efficiency)
    plt.xlabel('#cores')
    plt.ylabel(ylabel)
    plt.xscale(xscale)
    plt.yscale(yscale)
    plt.grid(grid, which='both')
    plt.tight_layout()
    
    return plt
