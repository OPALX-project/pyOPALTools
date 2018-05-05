from opal.datasets.filetype import FileType
from opal.datasets.DatasetBase import DatasetBase
from opal.analysis.cyclotron import *
import numpy as np
import matplotlib.pyplot as plt

def plot_orbits(ds, pid=0, **kwargs):
    """
    Do an orbit plot. Only with datasets of
    type FileType.TRACK_ORBIT.
    
    Parameters
    ----------
    ds      (DatasetBase)   datasets
    
    Optional parameters
    -------------------
    pid     (int)           which particle id
                            (default: 0)
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.TRACK_ORBIT:
        raise TypeError(ds.filename + ' is not a track orbit dataset.')
    
    xdata = ds.getData('x')
    ydata = ds.getData('y')
    ids   = ds.getData('ID')
    
    xdata = xdata[np.where(ids == pid)]
    ydata = ydata[np.where(ids == pid)]
    
    plt.plot(xdata, ydata)
    
    xlabel = ds.getLabel('x')
    xunit  = ds.getUnit('x')
    
    ylabel = ds.getLabel('y')
    yunit  = ds.getUnit('y')
    
    plt.xlabel(xlabel + ' [' + xunit + ']')
    plt.ylabel(ylabel + ' [' + yunit + ']')
    
    return plt


def plot_centering(ds, **kwargs):
    """
    Only with datasets of
    type FileType.TRACK_ORBIT.
    
    Parameters
    ----------
    ds      (DatasetBase)   datasets
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.TRACK_ORBIT:
        raise TypeError(ds.filename + ' is not a track orbit dataset.')
    
    
    _, _, _, radius = calcTurnSeparation(ds)
    
    x = calcCenteringExtraction(radius)
    
    plt.plot(x[2], x[3], 'o', **kwargs)
    
    ax = plt.gca()
    
    # Add circles
    circle1 = plt.Circle((0, 0), radius=2, fc='black', fill=False)
    plt.gca().add_artist(circle1)
    circle2 = plt.Circle((0, 0), radius=4, fc='black', fill=False)
    plt.gca().add_artist(circle2)
    
    # Move left y-axis and bottim x-axis to centre, passing through (0,0)
    ax.set_xlim(-5,5)
    ax.set_ylim(-5,5)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    # Eliminate upper and right axes
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    
    # Show ticks in the left and lower axes only
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    plt.xlabel('E')
    plt.ylabel('F')
    ax.xaxis.set_label_coords(0.9, -0.025)
    ax.yaxis.set_label_coords(-0.025,0.9)

    return plt

def plot_turns(ds, **kwargs):
    """
    Only with datasets of
    type FileType.TRACK_ORBIT.
    
    Parameters
    ----------
    ds      (DatasetBase)   datasets
    
    Returns
    -------
    a matplotlib.pyplot handle
    """

    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.TRACK_ORBIT:
        raise TypeError(ds.filename + ' is not a track orbit dataset.')
    
    _, _, _, radius = calcTurnSeparation(ds)
    
    plt.plot(np.arange(2, len(radius)+2), radius, **kwargs)
    plt.xlabel('Turn Number')
    plt.ylabel('Radius [m]')
    
    return plt

def plot_turn_separation(ds, nsteps=-1, asFunctionOfTurnNumber=True, asFunctionOfEnergy=False,**kwargs):
    """
    Only with datasets of
    type FileType.TRACK_ORBIT.
    
    Parameters
    ----------
    ds      (DatasetBase)   datasets
    nsteps                  number of steps per turn

    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.TRACK_ORBIT:
        raise TypeError(ds.filename + ' is not a track orbit dataset.')
    
    ts, energy, _, radius = calcTurnSeparation(ds, nsteps)
    
    if asFunctionOfTurnNumber:
        x = np.arange(2, len(ts)+2) # From second turn
        plt.xlabel('Turn Number')
    elif asFunctionOfEnergy:
        x = energy[1:] # From second turn
        plt.xlabel('Energy [MeV]')
    else:
        x = radius[1:] # From second turn, in meters
        plt.xlabel('Radius [m]')

    plt.plot(x, ts, 'o-', linewidth=2, **kwargs)
    plt.ylabel('Turn Separation [mm]')
    
    return plt


def plot_beta_beat(ds, **kwargs):
    """
    Only with datasets of
    type FileType.TRACK_ORBIT.
    
    Parameters
    ----------
    ds      (DatasetBase)   datasets
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.TRACK_ORBIT:
        raise TypeError(ds.filename + ' is not a track orbit dataset.')
    
    _, _, phi, radius = calcTurnSeparation(ds)

    plt.plot(radius, phi, 'o-', linewidth=2, **kwargs)
    plt.xlabel('Radius [m]')
    plt.ylabel('Radial Direction [rad]')
    
    return plt
    

def plot_RF_phases(ds, RFcavity, **kwargs):
    """
    Only with datasets of
    type FileType.OUTPUT.
    
    Parameters
    ----------
    ds          (DatasetBase)   datasets
    RFcavity    ([str])         name of the RFcavity as specifed in the input file
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.OUTPUT:
        raise TypeError(ds.filename + ' is not an OPAL standard output file.')
    
    data = calcRFphases(ds, RFcavity)
    
    for i, cname in enumerate(RFcavity):
        turns  = data[i][0]
        phases = data[i][1]
        plt.plot(turns, phases, linewidth=3, label=cname, **kwargs)
    plt.xlabel("Turn number")
    plt.ylabel("RF phase [deg]")
    plt.legend(loc=0)
    
    return plt


def plot_peak_difference(dsets, **kwargs):
    """
    Plot the peak difference of a probe output.
    This function works for FileType.PEAK (*.peaks)
    files.
    
    Parameters
    ----------
    dsets   (DatasetBase)   2 datasets
    
    Optionals
    ---------
    grid    (bool)          draw grid
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not len(dsets) == 2:
        raise ValueError('Exactly 2 datasets expected. ' +
                         'len(dsets) = ' + str(len(dsets)) + ' != 2.')
    
    for ds in dsets:
        if not isinstance(ds, DatasetBase):
            raise TypeError("Dataset '" + ds.filename +
                            "' not derived from 'DatasetBase'.")
    
        if not ds.filetype == FileType.PEAK:
            raise TypeError(ds.filename +
                            ' is not a peak (*.peaks) file.')
    
    unit = dsets[0].getUnit('radius')
    
    if not unit == dsets[1].getUnit('radius'):
        raise ValueError('Not same radius units.')
    
    peaks1 = dsets[0].getData('radius')
    peaks2 = dsets[1].getData('radius')
    
    npeaks = min(len(peaks1), len(peaks2))
    diff = peaks1[0:npeaks] - peaks2[0:npeaks]
    
    
    xticks = range(1, npeaks + 1)
    
    #ylim = [min(diff) - 0.001, max(diff) + 0.001]
    
    plt.plot(xticks, diff, 'o')
    plt.xticks(xticks)
    #plt.ylim(ylim)
    plt.grid(kwargs.get('grid', False))
    
    plt.xlabel('peak number')
    
    plt.ylabel('peak difference [' + unit + ']')
    
    return plt


def plot_probe_histogram(ds, **kwargs):
    """
    Plot a histogram of the probe histogram
    bin count vs. radius.
    
    Parameters
    ----------
    ds      (DatasetBase)   dataset
    
    Optionals
    ---------
    grid    (bool)          draw grid
    scale   (bool)          scales to 1.0
                            (default: False)
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.HIST:
        raise TypeError(ds.filename +
                        ' is not a probe histogram (*.hist) file.')
    
    bincount = ds.getData('bincount')
    rmin = ds.getData('min')
    rmax = ds.getData('max')
    nbins = ds.getData('nbins')
    #dr = ds.getData('binsize')
    
    radius = np.linspace(float(rmin), float(rmax), nbins)
    
    ylabel = ds.getLabel('bincount')
    
    if kwargs.get('scale', False):
        bincount = np.asarray(bincount) / max(bincount )
        ylabel += ' (normalized)'
    
    plt.plot(radius, bincount)
    plt.xlabel('radius [' + ds.getUnit('min') + ']')
    plt.ylabel(ylabel)
    plt.grid(kwargs.get('grid', False))
    
    return plt