from opal.analysis.Statistics import Statistics
import dask.array as da
import dask
from dask.array import stats
import scipy as sc
from opal.utilities.logger import opal_logger

class H5Statistics(Statistics):

    def _select(self, data, attrval, val, step):
        """
        Take a slice from the array

        Parameters
        ----------
        data    (dask.array)    container to extract data from
        attrval (dask.array)    data compare with in extraction value
        val     (int/float)     value for extraction comparison
        step    (int)           step in H5 file

        Notes
        -----
        There is an open issue on chunking. After taking a slice
        of the array, the shape is NaN causing errors. It needs
        to be rechunked.

        Open issue:
        https://github.com/dask/dask/issues/3293

        Returns
        -------
        slice of data
        """
        data = da.compress(val == attrval, data)
        data = data.compute()
        data = da.from_array(data, chunks='auto')

        if data.size < 1:
            raise ValueError('Empty data container.')

        return data


    def _selectBunch(self, data, bunch, step):
        """
        Take a slice from the array

        Notes
        -----
        There is an open issue on chunking. After taking a slice
        of the array, the shape is NaN causing errors. It needs
        to be rechunked.

        Open issue:
        https://github.com/dask/dask/issues/3293
        """
        if bunch > -1:
            bunchnum = self.ds.getData('bunchNumber', step=step)
            data = self._select(data, bunchnum, bunch, step)

        return data


    def moment(self, var, k, **kwargs):
        """
        Calculate the k-th central moment.
        
        Parameters
        ----------
        var     (str)           the variable to compute k-th central moment
        k       (int)           the moment, k = 1 is central mean
        
        Optionals
        ---------
        step    (int)           of dataset
        bunch   (int)           for which bunch to compute
        
        Notes
        -----
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.moment.html#scipy.stats.moment
        """
        step  = kwargs.pop('step', 0)
        bunch = kwargs.pop('bunch', -1)

        data = self.ds.getData(var, step=step)

        data = self._selectBunch(data, bunch, step)

        return stats.moment(data, axis=0, moment=k).compute().item(0)


    def mean(self, var, **kwargs):
        """
        Calculate the arithmetic mean.
        
        Parameters
        ----------
        var     (str)           the variable to compute mean
        
        Optionals
        ---------
        step    (int)           of dataset
        bunch   (int)           for which bunch to compute
        """
        step  = kwargs.pop('step', 0)
        bunch = kwargs.pop('bunch', -1)

        data = self.ds.getData(var, step=step)

        data = self._selectBunch(data, bunch, step)
            
        return data.mean(axis=0).compute()


    def skew(self, var, **kwargs):
        """
        Calculate the skewness.
        
        23. March 2018
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.skew.html#scipy.stats.skew
        
        Parameters
        ----------
        var     (str)           the variable
        
        Optionals
        ---------
        step    (int)           of dataset
        bunch   (int)           for which bunch to compute
        """
        step  = kwargs.pop('step', 0)
        bunch = kwargs.pop('bunch', -1)

        data = self.ds.getData(var, step=step)

        data = self._selectBunch(data, bunch, step)
        
        return stats.skew(data, axis=0).compute().item(0)


    def kurtosis(self, var, **kwargs):
        """
        23. March 2018
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kurtosis.html#scipy.stats.kurtosis
        
        Compute the kurtosis (Fisher or Pearson) of a dataset.
        
        Kurtosis is the fourth central moment divided by the square of the variance.
        Fisher’s definition is used, i.e. 3.0 is subtracted from the result to give 0.0
        for a normal distribution.
        
        Parameters
        ----------
        var     (str)           the variable
        
        Optionals
        ---------
        step    (int)           of dataset
        bunch   (int)           for which bunch to compute
        """
        opal_logger.error('dask.stats.kurtosis does not agree with scipy.stats.kurtosis')

        step  = kwargs.pop('step', 0)
        bunch = kwargs.pop('bunch', -1)

        data = self.ds.getData(var, step=step)

        data = self._selectBunch(data, bunch, step)
        
        return stats.kurtosis(data, axis=0, fisher=True).compute().item(0)


    def gaussian_kde(self, var, **kwargs):
        """
        23. March 2018
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.html#scipy.stats.gaussian_kde
        
        Representation of a kernel-density estimate using Gaussian kernels.
        
        Parameters
        ----------
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
        step    = kwargs.pop('step', 0)
        data = self.ds.getData(var, step=step)

        return dask.delayed(sc.stats.gaussian_kde)(data)


    def histogram(self, var, bins, range, **kwargs):
        """
        Compute a histogram of a dataset
        
        Parameters
        ----------
        var     (str)           the variable
        bins    (int)           number of bins
        range   ([])            range of histogram

        Optionals
        ---------
        step    (int)           of dataset
                                (see https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.histogram.html)
        density (bool)          normalize such that integral over
                                range is 1.
                                
        Returns
        -------
        a numpy.histogram with bin edges
        (see https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.histogram.html)
        """
        step    = kwargs.pop('step', 0)
        
        data = self.ds.getData(var, step=step)
        density = kwargs.pop('density', True)

        return da.histogram(data, bins=bins, range=range, density=density)


    def halo_continuous_beam(self, var, **kwargs):
        """
        Compute the halo in horizontal or
        vertical direction according to
        
        h_x = <x^4> / <x^2>^2 - 2
        
        Parameters
        ----------
        var     (str)           the variable
        
        Optionals
        ---------
        step    (int)           of dataset
        bunch   (int)           for which bunch to compute
        
        Reference
        ---------
        T. P. Wangler, Los Alamos National Laboratory, Los Alamos, NM 87545,
        K. R. Crandall, TechSource, Santa Fe, NM 87594-1057,
        BEAM HALO IN PROTON LINAC BEAMS,
        XX International Linac Conference, Monterey, California
        """
        step    = kwargs.pop('step', 0)
        bunch = kwargs.pop('bunch', -1)

        data = self.ds.getData(var, step=step)

        data = self._selectBunch(data, bunch, step)

        m4 = stats.moment(data, moment=4)
        m2 = stats.moment(data, moment=2)
        return (m4 / m2 ** 2 - 2.0).compute().item(0)


    def halo_ellipsoidal_beam(self, var, **kwargs):
        """
        Compute the halo in horizontal, vertical
        or longitudinal direction according to
        
        h_x = <x^4> / <x^2>^2 - 15 / 17
        
        Parameters
        ----------
        var     (str)           the variable
        
        Optionals
        ---------
        step    (int)           of dataset
        bunch   (int)           for which bunch to compute
        
        Reference
        ---------
        T. P. Wangler, Los Alamos National Laboratory, Los Alamos, NM 87545,
        K. R. Crandall, TechSource, Santa Fe, NM 87594-1057,
        BEAM HALO IN PROTON LINAC BEAMS,
        XX International Linac Conference, Monterey, California
        """
        step = kwargs.pop('step', 0)
        bunch = kwargs.pop('bunch', -1)

        data = self.ds.getData(var, step=step)

        data = self._selectBunch(data, bunch, step)

        m4 = stats.moment(data, moment=4)
        m2 = stats.moment(data, moment=2)

        return (m4 / m2 ** 2 - 15.0 / 7.0).compute().item(0)


    def projected_emittance(self, dim, **kwargs):
        """
        Compute the projected emittance. It shifts the
        coordinates by their mean value such that the bunch
        is centered around zero.
        
        \varepsilon = \sqrt{ <coords^2><momenta^2> - <coords*momenta>^2 }
        
        Parameters
        ----------
        dim     (str)           the dimension 'x', 'y' or 'z'
        
        Optionals
        ---------
        step    (int)           of dataset
        bunch   (int)           for which bunch to compute
        
        Returns
        -------
        the projected emittance
        """
        step = kwargs.pop('step', 0)
        
        coords = self.ds.getData(dim, step=step)
        momenta = self.ds.getData('p' + dim, step=step)
        
        bunch = kwargs.pop('bunch', -1)

        coords  = self._selectBunch(coords, bunch, step)
        momenta = self._selectBunch(momenta, bunch, step)

        c2 = stats.moment(coords, moment=2)
        m2 = stats.moment(momenta, moment=2)

        # we need to shift coords to center the beam
        coords -= coords.mean(axis=0)

        cm = (coords * momenta).mean(axis=0)

        return da.sqrt( m2 * c2 - cm ** 2 ).compute()


    def find_beams(self, var, **kwargs):
        """
        Compute the starting and end points of a beam via
        a histogram.
        The purpose of this script is to distinguish bunches
        of a multi-bunch simulation.
        
        Parameters
        ----------
        var     (str)           the variable
        
        Optionals
        ---------
        step    (int)           of dataset
        bins    (int)           number of bins for histogram
        
        Returns
        -------
        a list of minima locations and corresponding histogram
        """
        step = kwargs.pop('step', 0)
        bins = kwargs.pop('bins', 20)
        Wn   = kwargs.pop('Wn', 0.15)
        bins = kwargs.pop('bins', 100)
        
        data = self.ds.getData(var, step=step)

        if data.size < 1:
            raise ValueError('Empty data container.')

        dmin = da.min(data)
        dmax = da.max(data)
        data, bin_edges = da.histogram(data, bins=bins, range=[dmin, dmax])

        # smooth
        from scipy import signal
        b, a = signal.butter(1, Wn=Wn, btype='lowpass')
        data_smoothed = dask.delayed(signal.filtfilt)(b, a, data)


        from scipy.signal import find_peaks
        ymax = dask.delayed(max)(data_smoothed)

        # we need to compute here otherwise find_peaks
        # does not work
        tmp = (-data_smoothed + ymax).compute()

        peak_indices, _ = find_peaks(tmp, height=0)
        return peak_indices, data, bin_edges


    def rotate(x, y, theta):
        """
        Rotate the coordinates (x, y) by theta (degree)

        Parameters
        ----------
        x       (dask.array) is x-data
        y       (dask.array) is y-data
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