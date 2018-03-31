# Author:   Matthias Frey
# Date:     March 2018

from opal.statistics import statistics as stat
import numpy as np
import scipy as sc
from scipy.signal import argrelmin

def halo_continuous_beam(ds, var, **kwargs):
    """
    Compute the halo in horizontal or
    vertical direction according to
    
    h_x = <x^4> / <x^2>^2 - 2
    
    Parameters
    ----------
    ds      (DatasetBase)   datasets
    var     (str)           the variable
    
    Optionals
    ---------
    see opal.statistics.moment
    
    Reference
    ---------
    T. P. Wangler, Los Alamos National Laboratory, Los Alamos, NM 87545,
    K. R. Crandall, TechSource, Santa Fe, NM 87594-1057,
    BEAM HALO IN PROTON LINAC BEAMS,
    XX International Linac Conference, Monterey, California
    """
    m4 = stat.moment(ds, var, k=4, **kwargs)
    m2 = stat.moment(ds, var, k=2, **kwargs)
    
    return m4 / m2 ** 2 - 2.0


def halo_ellipsoidal_beam(ds, var, **kwargs):
    """
    Compute the halo in horizontal, vertical
    or longitudinal direction according to
    
    h_x = <x^4> / <x^2>^2 - 15 / 17
    
    Parameters
    ----------
    ds      (DatasetBase)   datasets
    var     (str)           the variable
    
    Optionals
    ---------
    see opal.statistics.moment
    
    Reference
    ---------
    T. P. Wangler, Los Alamos National Laboratory, Los Alamos, NM 87545,
    K. R. Crandall, TechSource, Santa Fe, NM 87594-1057,
    BEAM HALO IN PROTON LINAC BEAMS,
    XX International Linac Conference, Monterey, California
    """
    m4 = stat.moment(ds, var, k=4, **kwargs)
    m2 = stat.moment(ds, var, k=2, **kwargs)
    
    return m4 / m2 ** 2 - 15.0 / 7.0


def find_beams(ds, var, **kwargs):
    """
    Compute the starting and end points of a beam via
    kernel density estimation and the calculation of
    relative minima of the dataset.
    The purpose of this script is to distinguish bunches
    of a multi-bunch simulation.
    
    Parameters
    ----------
    ds      (DatasetBase)   datasets
    var     (str)           the variable
    
    Optionals
    ---------
    step    (int)           of dataset
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
    
    step    = kwargs.get('step', 0)
    npoints = kwargs.get('npoints', 500)
    
    data = ds.getData(var, step=step)
    
    kde = sc.stats.gaussian_kde(data)
    
    xmin = min(data)
    xmax = max(data)
    points = np.linspace(xmin, xmax, npoints)
    
    pdf = kde.pdf(points)
    
    extrema = argrelmin(pdf)
    
    bc = [xmin]
    for idx in extrema[0]:
        bc.append(points[idx])
    bc.append(xmax)
    
    return bc
