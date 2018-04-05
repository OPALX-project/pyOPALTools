from opal.datasets.DatasetBase import DatasetBase, FileType
from opal.analysis.cyclotron import *
import numpy as np
import matplotlib.pyplot as plt

def plot_orbits(ds, **kwargs):
    """
    Do an orbit plot. Only with datasets of
    type FileType.TRACK_ORBIT.
    
    Parameters
    ----------
    ds      (DatasetBase)   datasets
    
    Optional parameters
    -------------------
    id      (int)           which particle id
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
    
    pid = kwargs.get('id', 0)
    
    if not pid:
        raise ValueError("No data for particle id '" + str(pid) + "'.")
    
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


def plot_turn_separation(ds, asFunctionOfTurnNumber=True, asFunctionOfEnergy=False,**kwargs):
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
    
    ts, energy, _, radius = calcTurnSeparation(ds)
    
    if asFunctionOfTurnNumber:
        x = np.arange(2, len(ts)+2) # From second turn
        plt.xlabel('Turn Number')
    elif asFunctionOfEnergy:
        x = energy[1:] # From second turn
        plt.xlabel('Energy [MeV]')
    else:
        x = radius[1:] / 1000. # From second turn, in meters
        plt.xlabel('Radius [m]')

    plt.plot(x, ts, 'o-', linewidth=2, **kwargs)
    plt.ylabel('Turn Separation [mm]')
    
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
