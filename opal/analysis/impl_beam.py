from opal.analysis.Statistics import Statistics
import numpy as np
import dask.array as da
from opal.analysis import cyclotron

def find_beams(data, **kwargs):
    """
    Implementation of find beams. Operates direclty
    on data.
    
    Parameters
    ----------
    data    (list, array)   is plain data
    
    Optionals
    ---------
    bins (int)              number of bins for histogram
    
    Returns
    -------
    a list of minima locations and corresponding histogram
    """
    if data.size < 1:
        raise ValueError('Empty data container.')
    
    bins = kwargs.get('bins', 20)
    
    dmin = da.min(data)
    dmax = da.max(data)
    hist = da.histogram(data, bins=bins, range=[dmin, dmax], density=True)

    inv_hist = -hist[0]

    extrema = cyclotron.detect_peaks(inv_hist)
    xmin = da.min(hist[1])
    xmax = da.max(hist[1])
    
    bc = [xmin]
    for idx in extrema:
        bc.append(hist[1][idx])
    bc.append(xmax)
    
    return bc, hist


def rotate(x, y, theta):
    """
    Rotate the coordinates (x, y) by theta (degree)
    
    Parameters
    ----------
    x       (array) is x-data
    y       (array) is y-data
    theta   (float) is the angle in degree
    
    
    Note
    ----
    
    R(theta) = [ cos(theta), -sin(theta)
                 sin(theta), cos(theta) ]
    
    [rx, ry] = R(theta) * [x, y]
    
    Reference
    ---------
    https://en.wikipedia.org/wiki/Rotation_matrix
    
    Returns
    -------
    rotated coordinates (rx, ry)
    """
    
    theta = da.deg2rad(theta)
    
    cos = da.cos(theta)
    sin = da.sin(theta)
    
    rx = x * cos - y * sin
    ry = x * sin + y * cos
    
    return rx, ry
