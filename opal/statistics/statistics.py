import numpy as np
from opal.datasets.filetype import FileType
from opal.statistics import impl_statistics

def moment(ds, var, k, **kwargs):
    """
    Calculate the k-th central moment.
    
    Parameters
    ----------
    ds      (DatasetBase)   where the data is taken from
    var     (str)           the variable to compute k-th central moment
    k       (int)           the moment, k = 1 is central mean
    
    Optionals
    ---------
    step    (int)           of dataset
    bin     (int)           energy bin for which to compute
    
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
    
    return impl_statistics.moment(data, k)


def mean(ds, var, **kwargs):
    """
    Calculate the arithmetic mean.
    
    Parameters
    ----------
    ds      (DatasetBase)   where the data is taken from
    var     (str)           the variable to compute mean
    
    Optionals
    ---------
    step    (int)           of dataset
    bin     (int)           energy bin for which to compute
    """
    step = kwargs.get('step', 0)
    
    data = ds.getData(var, step=step)
    
    energy_bin = kwargs.get('bin', -1)
    if energy_bin > 0 and ds.filetype == FileType.H5:
        bins = ds.getData('bin', step=step)
        data = data[np.where(bins == energy_bin)]
        
    return impl_statistics.mean(data)


def skew(ds, var, **kwargs):
    """
    Calculate the skewness.
    
    23. March 2018
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.skew.html#scipy.stats.skew
    
    Parameters
    ----------
    ds      (DatasetBase)   where the data is taken from
    var     (str)           the variable
    
    Optionals
    ---------
    step    (int)           of dataset
    bin     (int)           energy bin for which to compute
    """
    step = kwargs.get('step', 0)
    
    data = ds.getData(var, step=step)
    
    energy_bin = kwargs.get('bin', -1)
    if energy_bin > 0 and ds.filetype == FileType.H5:
        bins = ds.getData('bin', step=step)
        data = data[np.where(bins == energy_bin)]
    
    return impl_statistics.skew(data)


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
    
    Optionals
    ---------
    step    (int)           of dataset
    bin     (int)           energy bin for which to compute
    """
    step = kwargs.get('step', 0)
    
    data = ds.getData(var, step=step)
    
    energy_bin = kwargs.get('bin', -1)
    if energy_bin > 0 and ds.filetype == FileType.H5:
        bins = ds.getData('bin', step=step)
        data = data[np.where(bins == energy_bin)]
    
    return impl_statistics.skew(data)


def gaussian_kde(ds, var, **kwargs):
    """
    23. March 2018
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.html#scipy.stats.gaussian_kde
    
    Representation of a kernel-density estimate using Gaussian kernels.
    
    Parameters
    ----------
    ds      (DatasetBase)   where the data is taken from
    var     (str)           the variable
    
    Optionals
    ---------
    step    (int)           of dataset
    bins    (int /str)      binning type or #bins
                            (see https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.histogram.html)
    density (bool)          normalize such that integral over
                            range is 1.
    
    Returns
    -------
    kernel density estimator of scipy.
    """
    step    = kwargs.get('step', 0)
    bins    = kwargs.get('bins', 'sturges')
    density = kwargs.get('density', True)
    
    data = ds.getData(var, step=step)
    
    return impl_statistics.gaussian_kde(data)


def histogram(ds, var, **kwargs):
    """
    Compute a histogram of a dataset
    
    Parameters
    ----------
    ds      (DatasetBase)   where the data is taken from
    var     (str)           the variable
    
    Optionals
    ---------
    step    (int)           of dataset
    bins    (int /str)      binning type or #bins
                            (see https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.histogram.html)
    density (bool)          normalize such that integral over
                            range is 1.
                            
    Returns
    -------
    a numpy.histogram with bin edges
    (see https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.histogram.html)
    """
    step    = kwargs.get('step', 0)
    
    data = ds.getData(var, step=step)
    
    return impl_statistics.histogram(data, **kwargs)
