from opal.analysis.Statistics import Statistics
import numpy as np
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
    
    hist = np.histogram(data, bins=bins, density=True)
    
    inv_hist = -hist[0]

    extrema = cyclotron.detect_peaks(inv_hist)

    xmin = min(hist[1])
    xmax = max(hist[1])
    
    bc = [xmin]
    for idx in extrema:
        bc.append(hist[1][idx])
    bc.append(xmax)
    
    return bc, hist


def halo_continuous_beam(data):
    """
    Compute the halo in horizontal or
    vertical direction according to
    
    h_x = <x^4> / <x^2>^2 - 2
    
    Parameters
    ----------
    data    (list, array)   is plain data
    
    Reference
    ---------
    T. P. Wangler, Los Alamos National Laboratory, Los Alamos, NM 87545,
    K. R. Crandall, TechSource, Santa Fe, NM 87594-1057,
    BEAM HALO IN PROTON LINAC BEAMS,
    XX International Linac Conference, Monterey, California
    """
    if data.size < 1:
        raise ValueError('Empty data container.')
    
    stat = Statistics()
    
    m4 = stat.moment(data, k=4)
    m2 = stat.moment(data, k=2)
    
    return m4 / m2 ** 2 - 2.0


def halo_ellipsoidal_beam(data):
    """
    Compute the halo in horizontal, vertical
    or longitudinal direction according to
    
    h_x = <x^4> / <x^2>^2 - 15 / 7
    
    Parameters
    ----------
    data    (list, array)   is plain data
    
    Reference
    ---------
    T. P. Wangler, Los Alamos National Laboratory, Los Alamos, NM 87545,
    K. R. Crandall, TechSource, Santa Fe, NM 87594-1057,
    BEAM HALO IN PROTON LINAC BEAMS,
    XX International Linac Conference, Monterey, California
    """
    if data.size < 1:
        raise ValueError('Empty data container.')
    
    stat = Statistics()
    
    m4 = stat.moment(data, k=4)
    m2 = stat.moment(data, k=2)
    
    return m4 / m2 ** 2 - 15.0 / 7.0


def projected_emittance(coords, momenta):
    """
    Compute the projected emittance. It shifts the
    coordinates by their mean value such that the bunch
    is centered around zero.
    
    \varepsilon = \sqrt{ <coords^2><momenta^2> - <coords*momenta>^2 }
    """
    
    stat = Statistics()
    
    c2 = stat.moment(coords, k=2)
    m2 = stat.moment(momenta, k=2)
    
    # we need to shift coords to center the beam
    mean = stat.mean(coords)
    
    coords -= mean
    
    cm = np.mean(np.asarray(coords) * np.asarray(momenta))
    
    return np.sqrt( m2 * c2 - cm ** 2 )


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
    
    theta = np.deg2rad(theta)
    
    cos = np.cos(theta)
    sin = np.sin(theta)
    
    rx = x * cos - y * sin
    ry = x * sin + y * cos
    
    return rx, ry
