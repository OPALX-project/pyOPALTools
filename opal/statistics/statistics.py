import numpy as np
import scipy as sc
from opal.datasets.DatasetBase import FileType

def moment(ds, var, k, **kwargs):
    """
    Calculate the k-th central moment.
    
    
    Parameters
    ----------
    ds      (DatasetBase)   where the data is taken from
    var     (str)           the variable to compute k-th central moment
    k       (int)           the moment, k = 1 is central mean
    bin     (int)           energy bin for which to compute (optional)
    
    Notes
    -----
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.moment.html#scipy.stats.moment
    """
    step = kwargs.get('step', 0)
    
    data = ds.getData(var, step=step)
    
    energy_bin = kwargs.get('bin', -1)
    if energy_bin > 0 and ds.filetype == FileType.H5:
        bins = ds.getData('bin', step=step)
        data = data[np.where(bins == energy_bin)]
    
    if data.size < 1:
        raise RuntimeError('Empty dataset.')
    
    return sc.stats.moment(data, axis=0, moment=k)


def mean(ds, var, **kwargs):
    """
    Calculate the arithmetic mean.
    
    Parameters
    ----------
    ds      (DatasetBase)   where the data is taken from
    var     (str)           the variable to compute mean
    bin     (int)           energy bin for which to compute (optional)
    """
    step = kwargs.get('step', 0)
    
    data = ds.getData(var, step=step)
    
    energy_bin = kwargs.get('bin', -1)
    if energy_bin > 0 and ds.filetype == FileType.H5:
        bins = ds.getData('bin', step=step)
        data = data[np.where(bins == energy_bin)]
    
    if data.size < 1:
        raise RuntimeError('Empty dataset.')
    
    return np.mean(data, axis=0)


def skew(ds, var, **kwargs):
    """
    Calculate the skewness.
    
    23. March 2018
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.skew.html#scipy.stats.skew
    
    Parameters
    ----------
    ds      (DatasetBase)   where the data is taken from
    var     (str)           the variable
    bin     (int)           energy bin for which to compute (optional)
    """
    step = kwargs.get('step', 0)
    
    data = ds.getData(var, step=step)
    
    energy_bin = kwargs.get('bin', -1)
    if energy_bin > 0 and ds.filetype == FileType.H5:
        bins = ds.getData('bin', step=step)
        data = data[np.where(bins == energy_bin)]
    
    if data.size < 1:
        raise RuntimeError('Empty dataset.')
    
    return sc.stats.skew(data, axis=0)


def kurtosis(ds, var, **kwargs):
    """
    23. March 2018
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kurtosis.html#scipy.stats.kurtosis
    
    Compute the kurtosis (Fisher or Pearson) of a dataset.
    
    Kurtosis is the fourth central moment divided by the square of the variance.
    Fisher’s definition is used, i.e. 3.0 is subtracted from the result to give 0.0
    for a normal distribution.
    
    Parameters
    ----------
    ds      (DatasetBase)   where the data is taken from
    var     (str)           the variable
    bin     (int)           energy bin for which to compute (optional)
    """
    step = kwargs.get('step', 0)
    
    data = ds.getData(var, step=step)
    
    energy_bin = kwargs.get('bin', -1)
    if energy_bin > 0 and ds.filetype == FileType.H5:
        bins = ds.getData('bin', step=step)
        data = data[np.where(bins == energy_bin)]
    
    if data.size < 1:
        raise RuntimeError('Empty dataset.')
    
    return sc.stats.kurtosis(data, axis=0, fisher=True)


def gaussian_kde(ds, var, **kwargs):
    """
    23. March 2018
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.html#scipy.stats.gaussian_kde
    
    Representation of a kernel-density estimate using Gaussian kernels.
    
    Parameters
    ----------
    ds      (DatasetBase)   where the data is taken from
    var     (str)           the variable
    bin     (int)           energy bin for which to compute (optional)
    """
    
    step    = kwargs.get('step', 0)
    bins    = kwargs.get('bins', 'sturges')
    density = kwargs.get('density', True)
    
    data = ds.getData(var, step=step)
    
    return sc.stats.gaussian_kde(data)


def histogram(ds, var, **kwargs):
    
    step    = kwargs.get('step', 0)
    bins    = kwargs.get('bins', 'sturges')
    density = kwargs.get('density', True)
    
    data = ds.getData(var, step=step)
    
    return np.histogram(data, density=density, bins=bins)
