from opal.datasets.filetype import FileType
from opal.datasets.DatasetBase import DatasetBase
from opal.analysis.cyclotron import *
import numpy as np
import matplotlib.pyplot as plt
import os

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
    
    plt.plot(xdata, ydata, **kwargs)
    
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
    
    plt.plot(np.arange(2, len(radius)+2), radius, **kwargs) # From second turn
    plt.xlabel('Turn Number')
    plt.ylabel('Radius [m]')
    
    return plt

def plot_energy(ds, nsteps=-1, **kwargs):
    """
    Only with datasets of
    type FileType.TRACK_ORBIT.
    
    Parameters
    ----------
    ds      (DatasetBase)   datasets
    nsteps                  number of steps per turn (default -1: detect automatically)
    
    Returns
    -------
    a matplotlib.pyplot handle
    """

    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.TRACK_ORBIT:
        raise TypeError(ds.filename + ' is not a track orbit dataset.')

    _, energy, _, radius = calcTurnSeparation(ds,nsteps)

    plt.xlabel('Turn Number')
    plt.ylabel('Energy [MeV]')
    # From second turn
    plt.plot(np.arange(2, len(radius)+2), energy, linewidth=2, **kwargs)
    plt.show()


    return plt

def plot_energy_gain(ds, nsteps=-1, **kwargs):
    """
    Only with datasets of
    type FileType.TRACK_ORBIT.
    
    Parameters
    ----------
    ds      (DatasetBase)   datasets
    nsteps                  number of steps per turn (default -1: detect automatically)
    
    Returns
    -------
    a matplotlib.pyplot handle
    """

    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.TRACK_ORBIT:
        raise TypeError(ds.filename + ' is not a track orbit dataset.')

    _, energy, _, radius = calcTurnSeparation(ds, nsteps)

    x = np.arange(2, len(radius)+1)
    y = np.diff(energy)
    plt.xlabel('Turn Number')
    plt.ylabel('Energy Gain [MeV]')
    # From second turn
    plt.plot(x, y, linewidth=2, **kwargs)
    plt.show()


    return plt

def plot_turn_separation(ds, nsteps=-1, angle=0.0, asFunctionOfTurnNumber=True, asFunctionOfEnergy=False,**kwargs):
    """
    Only with datasets of
    type FileType.TRACK_ORBIT.
    
    Parameters
    ----------
    ds      (DatasetBase)   datasets
    nsteps                  number of steps per turn (default -1: detect automatically)
    angle                   angle of reference line in radians

    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.TRACK_ORBIT:
        raise TypeError(ds.filename + ' is not a track orbit dataset.')
    
    ts, energy, _, radius = calcTurnSeparation(ds, nsteps, angle)
    
    if asFunctionOfTurnNumber:
        x = np.arange(2, len(ts)+2) # From second turn
        plt.xlabel('Turn Number')
    elif asFunctionOfEnergy:
        x = energy[1:] # From second turn
        plt.xlabel('Energy [MeV]')
    else:
        x = radius[1:] # From second turn, in meters
        plt.xlabel('Radius [m]')

    plt.plot(x, ts, linewidth=2, **kwargs)
    plt.ylabel('Turn Separation [mm]')
    
    return plt

def plot_beta_beat(ds, nsteps=-1, **kwargs):
    """
    Only with datasets of
    type FileType.TRACK_ORBIT.
    
    Parameters
    ----------
    ds      (DatasetBase)   datasets
    nsteps                  number of steps per turn (default -1: detect automatically)

    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.TRACK_ORBIT:
        raise TypeError(ds.filename + ' is not a track orbit dataset.')
    
    _, _, phi, radius = calcTurnSeparation(ds,nsteps)
    
    
    angle_unit = kwargs.pop('angle_unit', 'rad')
    
    if 'deg' in angle_unit:
        phi = np.degrees(phi)
        angle_unit == 'deg'
    
    plt.plot(radius, phi, 'o-', linewidth=2, **kwargs)
    plt.xlabel('Radius [m]')
    plt.ylabel('Radial Direction [' + angle_unit + ']')
    
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
    raxis   (bool)          do radius vs radius plot instead
    
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
    p1 = peaks1[0:npeaks]
    p2 = peaks2[0:npeaks]
    
    plt.grid(kwargs.pop('grid', False))
    
    if kwargs.pop('raxis'):
        lowest = min(min(p1), min(p2))
        highest = max(max(p1), max(p2))
        
        plt.plot([lowest, highest], [lowest, highest],
                 linestyle='dashed', color='black',
                 label='y = x')
        
        plt.plot(p1, p2, marker='o', **kwargs)
        
        plt.xlabel('radius [' + unit + '] (' +
                   os.path.basename(dsets[0].filename) + ')')
        plt.ylabel('radius [' + unit + '] (' +
                   os.path.basename(dsets[1].filename) + ')')
    else:
        diff = p1 - p2
    
        xticks = range(1, npeaks + 1)
        
        #ylim = [min(diff) - 0.001, max(diff) + 0.001]
    
        plt.plot(xticks, diff, 'o', **kwargs)
        plt.xticks(xticks)
        #plt.ylim(ylim)
        
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
    
    if kwargs.pop('scale', False):
        bincount = np.asarray(bincount) / max(bincount )
        ylabel += ' (normalized)'
    
    plt.grid(kwargs.pop('grid', False))

    plt.plot(radius, bincount, **kwargs)
    plt.xlabel('radius [' + ds.getUnit('min') + ']')
    plt.ylabel(ylabel)
    
    return plt