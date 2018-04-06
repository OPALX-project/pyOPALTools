from opal.statistics import impl_statistics as stat
import scipy as sc
from scipy import signal
import numpy as np

def find_beams(data, **kwargs):
    """
    Implementation of find beams. Operates direclty
    on data.
    
    Parameters
    ----------
    data    (list, array)   is plain data
    
    Optionals
    ---------
    npoints (int)           number of points to evaluate
                            kernel density estimator
    
    References (31. March 2018)
    ---------------------------
    https://docs.scipy.org/doc/scipy-0.19.0/reference/generated/scipy.stats.gaussian_kde.html
    https://docs.scipy.org/doc/scipy-0.16.1/reference/generated/scipy.signal.argrelmin.html
    
    Returns
    -------
    a list of minima locations
    """
    if data.size < 1:
        raise ValueError('Empty data container.')
    
    npoints = kwargs.get('npoints', 500)
    
    kde = sc.stats.gaussian_kde(data)
    
    xmin = min(data)
    xmax = max(data)
    points = np.linspace(xmin, xmax, npoints)
    
    pdf = kde.pdf(points)
    
    extrema = signal.argrelmin(pdf)
    
    bc = [xmin]
    for idx in extrema[0]:
        bc.append(points[idx])
    bc.append(xmax)
    
    return bc


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
    c2 = stat.moment(coords, k=2)
    m2 = stat.moment(momenta, k=2)
    
    # we need to shift coords to center the beam
    mean = stat.mean(coords)
    
    coords -= mean
    
    cm = np.mean(np.asarray(coords) * np.asarray(momenta))
    
    return np.sqrt( m2 * c2 - cm ** 2 )
