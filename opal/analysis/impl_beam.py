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
