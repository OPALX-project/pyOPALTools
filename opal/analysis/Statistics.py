import dask
import dask.array as da
import scipy as sc
import numpy as np
    
class Statistics:
    """
    Base class for all statistic functions
    on datasets.
    It also provides functions on plain data.
    """
    def __init__(self):
        pass

    def moment(self, data, k):
        """
        Calculate the k-th central moment directly
        on data.
        
        Parameters
        ----------
        data    (dask.array)   is plain data
        k       (int)           the moment, k = 1 is central mean
        """
        if data.size < 1:
            raise ValueError('Empty data container.')
        
        return da.stats.moment(data, axis=0, moment=k)


    def mean(self, data):
        """
        Calculate the arithmetic mean directly
        on data.
        
        Parameters
        ----------
        data    (dask.array)   is plain data
        """
        if data.size < 1:
            raise ValueError('Empty data container.')
        
        return data.mean(axis=0)


    def skew(self, data):
        """
        Calculate the skewness directly on
        data.
        
        Parameters
        ----------
        data    (dask.array)   is plain data
        """
        if data.size < 1:
            raise ValueError('Empty data container.')
        
        return da.stats.skew(data, axis=0)


    def kurtosis(self, data):
        """
        Compute the kurtosis (Fisher or Pearson) directly
        on data.
        
        Parameters
        ----------
        data    (dask.array)   is plain data
        """
        if data.size < 1:
            raise ValueError('Empty data container.')
        
        return da.stats.kurtosis(data, axis=0, fisher=True)


    def gaussian_kde(self, data):
        """
        Calculate the kernel density estimator directly
        on data.
        
        Parameters
        ----------
        data    (dask.array)   is plain data
        
        Returns
        -------
        scipy kernel density estimator
        """
        if data.size < 1:
            raise ValueError('Empty data container.')
        
        return dask.delayed(sc.stats.gaussian_kde)(data)


    def histogram(self, data, bins, range, **kwargs):
        """
        Compute a histogram of a dataset
        
        Parameters
        ----------
        data    (dask.array)   is plain data
        bins    (int)          #bins
        range   ([])           range of histogram
        
        Optionals
        ---------
                                (see https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.histogram.html)
        density (bool)          normalize such that integral over
                                range is 1.
        
        Returns
        -------
        a numpy.histogram with bin edges
        (see https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.histogram.html)
        """
        density = kwargs.get('density', True)
        return da.histogram(data, bins=bins, range=range, density=density)
