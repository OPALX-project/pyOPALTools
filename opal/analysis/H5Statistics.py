from opal.analysis.Statistics import Statistics
import numpy as np
import scipy as sc
from opal.utilities.logger import opal_logger
from opal.analysis.cyclotron import eval_radius, eval_radial_momentum

class H5Statistics(Statistics):

    def _select(self, data, attrval, val):
        """
        Take a slice from the array

        Parameters
        ----------
        data    (array)         container to extract data from
        attrval (array)         data compare with in extraction value
        val     (int/float)     value for extraction comparison

        Returns
        -------
        slice of data
        """
        data = data[val == attrval]

        if data.size < 1:
            raise ValueError('Empty data container.')

        return data


    def _selectBunch(self, data, bunch, step):
        """
        Take a slice from the array

        Parameters
        -----------
        data    (array)         the data where to extract
        bunch   (int)           to select
        step    (int)           step in H5 file
        """
        if bunch > -1 and self.ds.isStepDataset('bunchNumber'):
            bunchnum = self.ds.getData('bunchNumber', step=step)
            data = self._select(data, bunchnum, bunch)

        return data

    def _selectData(self, var, **kwargs):
        step    = kwargs.get('step', 0)
        turn    = kwargs.get('turn', None)
        bunch   = kwargs.get('bunch', -1)

        if turn:
            # probe *.h5 have turn in dataset (step always 0)
            turns = self.ds.getData('turn')
            data = self.ds.getData(var)
            data = self._select(data, turns, turn)
        else:
            data = self.ds.getData(var, step=step)
            data = self._selectBunch(data, bunch, step)

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
        turn    (int)           of dataset
        bunch   (int)           for which to compute (only if 'turn'
                                not given (default: -1 --> all particles)
        
        Notes
        -----
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.moment.html#scipy.stats.moment
        """
        data = self._selectData(var, **kwargs)
        
        return sc.stats.moment(data, axis=0, moment=k)


    def mean(self, var, **kwargs):
        """
        Calculate the arithmetic mean.
        
        Parameters
        ----------
        var     (str)           the variable to compute mean
        
        Optionals
        ---------
        step    (int)           of dataset
        turn    (int)           of dataset
        bunch   (int)           for which to compute (only if 'turn'
                                not given (default: -1 --> all particles)
        """
        data = self._selectData(var, **kwargs)
            
        return np.mean(data, axis=0)


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
        turn    (int)           of dataset
        bunch   (int)           for which to compute (only if 'turn'
                                not given (default: -1 --> all particles)
        """
        data = self._selectData(var, **kwargs)
        
        return sc.stats.skew(data, axis=0)


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
        turn    (int)           of dataset
        bunch   (int)           for which to compute (only if 'turn'
                                not given (default: -1 --> all particles)
        """
        data = self._selectData(var, **kwargs)
        
        return sc.stats.kurtosis(data, axis=0, fisher=True)


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
        turn    (int)           of dataset
        bunch   (int)           for which to compute (only if 'turn'
                                not given (default: -1 --> all particles)
        
        Returns
        -------
        kernel density estimator of scipy.
        """
        data = self._selectData(var, **kwargs)

        return sc.stats.gaussian_kde(data)


    def histogram(self, var, bins, **kwargs):
        """
        Compute a histogram of a dataset
        
        Parameters
        ----------
        var     (str)           the variable
        bins    (int /str)      binning type or #bins
                                (see https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.histogram.html)

        Optionals
        ---------
        step    (int)           of dataset
        turn    (int)           of dataset
        bunch   (int)           for which to compute (only if 'turn'
                                not given (default: -1 --> all particles)
        density (bool)          normalize such that integral over
                                range is 1.
                                
        Returns
        -------
        a numpy.histogram with bin edges
        (see https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.histogram.html)
        """
        density = kwargs.pop('density', True)

        data = self._selectData(var, **kwargs)

        return np.histogram(data, bins=bins, density=density)


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
        turn    (int)           of dataset
        bunch   (int)           for which to compute (only if 'turn'
                                not given (default: -1 --> all particles)
        
        Reference
        ---------
        T. P. Wangler, Los Alamos National Laboratory, Los Alamos, NM 87545,
        K. R. Crandall, TechSource, Santa Fe, NM 87594-1057,
        BEAM HALO IN PROTON LINAC BEAMS,
        XX International Linac Conference, Monterey, California
        """
        data = self._selectData(var, **kwargs)

        m4 = sc.stats.moment(data, moment=4)
        m2 = sc.stats.moment(data, moment=2)
        return m4 / m2 ** 2 - 2.0


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
        turn    (int)           of dataset
        bunch   (int)           for which to compute (only if 'turn'
                                not given (default: -1 --> all particles)
        
        Reference
        ---------
        T. P. Wangler, Los Alamos National Laboratory, Los Alamos, NM 87545,
        K. R. Crandall, TechSource, Santa Fe, NM 87594-1057,
        BEAM HALO IN PROTON LINAC BEAMS,
        XX International Linac Conference, Monterey, California
        """
        data = self._selectData(var, **kwargs)

        m4 = sc.stats.moment(data, moment=4)
        m2 = sc.stats.moment(data, moment=2)

        return m4 / m2 ** 2 - 15.0 / 7.0


    def radial_halo_ellipsoidal_beam(self, **kwargs):
        """
        Compute the halo in radial direction
        according to

        h_r = <r^4> / <r^2>^2 - 15 / 17

        Parameters
        ----------
        None

        Optionals
        ---------
        step    (int)           of dataset
        turn    (int)           of dataset
        bunch   (int)           for which to compute (only if 'turn'
                                not given (default: -1 --> all particles)

        Reference
        ---------
        T. P. Wangler, Los Alamos National Laboratory, Los Alamos, NM 87545,
        K. R. Crandall, TechSource, Santa Fe, NM 87594-1057,
        BEAM HALO IN PROTON LINAC BEAMS,
        XX International Linac Conference, Monterey, California
        """
        x = self._selectData('x', **kwargs)
        y = self._selectData('y', **kwargs)

        r  = eval_radius(x, y)

        m4 = sc.stats.moment(r, moment=4)
        m2 = sc.stats.moment(r, moment=2)

        return m4 / m2 ** 2 - 15.0 / 7.0


    def halo_2d_ellipsoidal_beam(self, var, **kwargs):
        """
        Compute the 2D halo in horizontal, vertical
        or longitudinal direction according to

        H_i = sqrt(3) / 2  * sqrt(A) / B - 15 / 7

        A = <q^4><p^4> + 3 * <q^2p^2>^2 - 4 * <qp^3> * <q^3p>
        B = <q^2><p^2> - <qp>^2

        with coordinate q and momentum p. Specify either the
        'step' or 'turn' (probes only).

        Parameters
        ----------
        var   (str)     the direction 'x', 'y' or 'z'

        Optionals
        ---------
        step    (int)           of dataset
        turn    (int)           of dataset
        bunch   (int)           for which to compute (only if 'turn'
                                not given (default: -1 --> all particles)

        Reference
        ---------
        https://journals.aps.org/prab/abstract/10.1103/PhysRevSTAB.5.124202
        """
        q = self._selectData(var, **kwargs)
        p = self._selectData('p' + var, **kwargs)

        return self._halo_2d_ellipsoidal_beam(q, p)


    def radial_halo_2d_ellipsoidal_beam(self, azimuth, **kwargs):
        """
        Compute the 2D radial halo according to

        H_i = sqrt(3) / 2  * sqrt(A) / B - 15 / 7

        A = <r^4><p^4> + 3 * <r^2p^2>^2 - 4 * <rp^3> * <r^3p>
        B = <r^2><p^2> - <rp>^2

        with radius r and radial momentum p.

        Parameters
        ----------
        azimuth (float)         for radial halo only (in degree)

        Optionals
        ---------
        step    (int)           of dataset
        turn    (int)           of dataset
        bunch   (int)           for which to compute (only if 'turn'
                                not given (default: -1 --> all particles)

        Reference
        ---------
        https://journals.aps.org/prab/abstract/10.1103/PhysRevSTAB.5.124202
        """
        x = self._selectData('x', **kwargs)
        px = self._selectData('px', **kwargs)

        y = self._selectData('y', **kwargs)
        py = self._selectData('py', **kwargs)

        r  = eval_radius(x, y)

        azimuth = np.deg2rad(azimuth)

        pr = eval_radial_momentum(px, py, azimuth)

        return self._halo_2d_ellipsoidal_beam(r, pr)


    def _halo_2d_ellipsoidal_beam(self, q, p):
        """
        Compute the 2D halo in horizontal, vertical
        or longitudinal direction according to

        H_i = sqrt(3) / 2  * sqrt(A) / B - 15 / 7

        A = <q^4><p^4> + 3 * <q^2p^2>^2 - 4 * <qp^3> * <q^3p>
        B = <q^2><p^2> - <qp>^2

        with coordinate q and momentum p.

        Parameters
        ----------
        q     (array)   coordinate data
        p     (array)   momentum data

        Reference
        ---------
        https://journals.aps.org/prab/abstract/10.1103/PhysRevSTAB.5.124202
        """

        # make centered
        q = q - np.mean(q)
        p = p - np.mean(p)

        q2 = np.mean(q ** 2)
        q4 = np.mean(q ** 4)

        p2 = np.mean(p ** 2)
        p4 = np.mean(p ** 4)

        q1p1 = np.mean(q*p)
        q2p2 = np.mean(q**2 * p**2)
        q1p3 = np.mean(q * p**3)
        q3p1 = np.mean(q**3 * p)

        A = q4 * p4 + 3.0 * q2p2 ** 2 - 4.0 * q1p3 * q3p1
        B = q2 * p2 - q1p1 ** 2

        return 0.5 * np.sqrt(3.0 * A) / B - 15.0 / 7.0


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
        turn    (int)           of dataset
        bunch   (int)           for which to compute (only if 'turn'
                                not given (default: -1 --> all particles)
        
        Returns
        -------
        the projected emittance
        """
        coords  = self._selectData(dim, **kwargs)
        momenta = self._selectData('p' + dim, **kwargs)

        c2 = sc.stats.moment(coords, moment=2)
        m2 = sc.stats.moment(momenta, moment=2)

        # we need to shift coords to center the beam
        coords -= np.mean(coords, axis=0)

        cm = np.mean(coords * momenta, axis=0)

        return np.sqrt( m2 * c2 - cm ** 2 )


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
        Wn   = kwargs.pop('Wn', 0.15)
        bins = kwargs.pop('bins', 100)

        data = self.ds.getData(var, step=step)

        if data.size < 1:
            raise ValueError('Empty data container.')

        dmin = np.min(data)
        dmax = np.max(data)
        data, bin_edges = np.histogram(data, bins=bins)

        # smooth
        from scipy import signal
        b, a = signal.butter(1, Wn=Wn, btype='lowpass')
        data_smoothed = signal.filtfilt(b, a, data)


        from scipy.signal import find_peaks
        ymax = np.max(data_smoothed)
        tmp = -data_smoothed + ymax

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
