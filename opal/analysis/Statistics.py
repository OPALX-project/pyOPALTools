from scipy import stats
import numpy as np

class Statistics:
    """Base class for all statistic functions on datasets.

    It also provides functions on plain data.
    """
    def __init__(self):
        pass

    def moment(self, data, k):
        """Calculate the k-th central moment directly on data.

        Parameters
        ----------
        data : array_like
            Plain data
        k : int
            The moment number, k = 1 is central mean

        Returns
        -------
        float
            k-th central moment
        """
        if data.size < 1:
            raise ValueError('Empty data container.')

        return stats.moment(data, axis=0, moment=k)


    def mean(self, data):
        """Calculate the arithmetic mean directly on data.

        Parameters
        ----------
        data : array_like
            Plain data

        Returns
        -------
        float
            arithmetic mean
        """
        if data.size < 1:
            raise ValueError('Empty data container.')

        return np.mean(data, axis=0)


    def skew(self, data):
        """Calculate the skewness directly on data.

        Parameters
        ----------
        data : array_like
            Plain data

        Returns
        -------
        float
            skewness
        """
        if data.size < 1:
            raise ValueError('Empty data container.')

        return stats.skew(data, axis=0)


    def kurtosis(self, data):
        """Compute the kurtosis (Fisher or Pearson) directly on data.

        Parameters
        ----------
        data : array_like
            Plain data

        Returns
        -------
        float
            kurtosis
        """
        if data.size < 1:
            raise ValueError('Empty data container.')

        return stats.kurtosis(data, axis=0, fisher=True)


    def gaussian_kde(self, data):
        """Calculate the kernel density estimator directly on data.

        Parameters
        ----------
        data : array_like
            Plain data

        Returns
        -------
        scipy.stats.gaussian_kde
            scipy kernel density estimator
        """
        if data.size < 1:
            raise ValueError('Empty data container.')

        return stats.gaussian_kde(data)


    def histogram(self, data, **kwargs):
        """Compute a histogram of a dataset

        Parameters
        ----------
        data : array_like
            Plain data
        bins : int or str, optional
            Binning type or nr of bins (default: 'sturges')
            (see https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.histogram.html)
        density : bool, optional
            Normalize such that integral over range is 1 (default: True).

        Returns
        -------
        numpy.histogram : array
            The values of the histogram. See `density` and `weights` for a
            description of the possible semantics.
        bin_edges : array of dtype float
            Return the bin edges ``(length(hist)+1)``.

        Notes
        -----
            See https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.histogram.html
        """
        bins    = kwargs.get('bins', 'sturges')
        density = kwargs.get('density', True)

        return np.histogram(data, density=density, bins=bins)
