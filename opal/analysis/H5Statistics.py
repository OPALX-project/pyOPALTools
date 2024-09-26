# Copyright (c) 2019 - 2020, Matthias Frey, Paul Scherrer Institut, Villigen PSI, Switzerland
# All rights reserved
#
# Implemented as part of the PhD thesis
# "Precise Simulations of Multibunches in High Intensity Cyclotrons"
#
# This file is part of pyOPALTools.
#
# pyOPALTools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# You should have received a copy of the GNU General Public License
# along with pyOPALTools. If not, see <https://www.gnu.org/licenses/>.

from opal.analysis.Statistics import Statistics
import dask.array as da
import dask
from dask.array import stats
import scipy as sc
from opal.utilities.logger import opal_logger
from opal.analysis.cyclotron import eval_radius, eval_radial_momentum

class H5Statistics(Statistics):

    def _select(self, data, attrval, val):
        """Take a slice from the array

        Parameters
        ----------
        data : dask.array
            Container to extract data from
        attrval : dask.array
            Data to compare with in extraction value
        val : int or float
            Value for extraction comparison

        Notes
        -----
        There is an open issue on chunking. After taking a slice
        of the array, the shape is NaN causing errors. It needs
        to be rechunked.

        Open issue:
        https://github.com/dask/dask/issues/3293

        Returns
        -------
        array_like
            Slice of data
        """
        data = da.compress(val == attrval, data)
        data = data.compute()
        data = da.from_array(data, chunks='auto')

        if data.size < 1:
            raise ValueError('Empty data container.')

        return data


    def _selectBunch(self, data, bunch, step):
        """Take a bunch slice from the array

        Notes
        -----
        There is an open issue on chunking. After taking a slice
        of the array, the shape is NaN causing errors. It needs
        to be rechunked.

        Open issue:
        https://github.com/dask/dask/issues/3293

        Parameters
        ----------
        data : array_like
            The data where to extract
        bunch : int
            Bunch to select
        step : int
            Step in H5 file

        Returns
        -------
        array_like
            Slice of data
        """
        if bunch > -1 and self.ds.isStepDataset('bunchNumber', step):
            bunchnum = self.ds.getData('bunchNumber', step=step)
            data = self._select(data, bunchnum, bunch)

        return data

    def selectData(self, var, **kwargs):
        """Select subset of data

        Given a H5 dataset, select a subset using
        the attributes step (or turn) and bunch.

        Parameters
        -----------
        var : str
            Variable name
        bunch : int, optional
            Bunch to select (default: -1, which means all particles)
        step : int, optional
            Step in H5 file (default: 0)
        turn : int, optional
            Turn of dataset (default: None, which implies no specific turn selection)
            (probe H5 files only)

        Returns
        -------
        array_like
            Data array
        """
        step    = kwargs.get('step', 0)
        turn    = kwargs.get('turn', None)
        bunch   = kwargs.get('bunch', -1)

        if step < 0:
            step = self.ds.size - 1

        data = self.ds.getData(var, step=step)
        data = self._selectBunch(data, bunch, step)

        if turn and self.ds.isStepDataset('turn', step):
            # probe *.h5 have turn in dataset
            turns = self.ds.getData('turn', step=step)
            turns = self._selectBunch(turns, bunch, step)
            data = self._select(data, turns, turn)

        return data


    def moment(self, var, k, **kwargs):
        """Calculate the k-th central moment.

        Parameters
        ----------
        var : str
            The variable to compute k-th central moment
        k : int
            The moment number, k = 1 is central mean
        bunch : int, optional
            Bunch to select (default: -1, which means all particles)
        step : int, optional
            Step in H5 file (default: 0)
        turn : int, optional
            Turn of dataset (default: None, which implies no specific turn selection)
            (probe H5 files only)

        Returns
        -------
        float
            k-th central moment

        Notes
        -----
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.moment.html
        """
        data = self.selectData(var, **kwargs)

        return stats.moment(data, axis=0, moment=k).compute().item(0)


    def radial_moment(self, k, **kwargs):
        """Calculate the k-th central radial moment.

        Parameters
        ----------
        k : int
            The moment number, k = 1 is central mean
        bunch : int, optional
            Bunch to select (default: -1, which means all particles)
        step : int, optional
            Step in H5 file (default: 0)
        turn : int, optional
            Turn of dataset (default: None, which implies no specific turn selection)
            (probe H5 files only)

        Returns
        -------
        float
            k-th central radial moment

        Notes
        -----
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.moment.html
        """
        x = self.selectData('x', **kwargs)
        y = self.selectData('y', **kwargs)

        r  = eval_radius(x, y)

        return sc.stats.moment(r, axis=0, moment=k)


    def mean(self, var, **kwargs):
        """Calculate the arithmetic mean.

        Parameters
        ----------
        var : str
            The variable
        bunch : int, optional
            Bunch to select (default: -1, which means all particles)
        step : int, optional
            Step in H5 file (default: 0)
        turn : int, optional
            Turn of dataset (default: None, which implies no specific turn selection)
            (probe H5 files only)

        Returns
        -------
        float
            arithmetic mean
        """
        data = self.selectData(var, **kwargs)

        return data.mean(axis=0).compute()


    def skew(self, var, **kwargs):
        """Calculate the skewness.

        Parameters
        ----------
        var : str
            The variable
        bunch : int, optional
            Bunch to select (default: -1, which means all particles)
        step : int, optional
            Step in H5 file (default: 0)
        turn : int, optional
            Turn of dataset (default: None, which implies no specific turn selection)
            (probe H5 files only)

        Returns
        -------
        float
            skewness

        Notes
        -----
        23. March 2018
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.skew.html
        """
        data = self.selectData(var, **kwargs)

        return stats.skew(data, axis=0).compute().item(0)


    def kurtosis(self, var, **kwargs):
        """Compute the kurtosis (Fisher or Pearson) of a dataset.

        Kurtosis is the fourth central moment divided by the square of the variance.
        Fisher’s definition is used, i.e. 3.0 is subtracted from the result to give 0.0
        for a normal distribution.

        Parameters
        ----------
        var : str
            The variable
        bunch : int, optional
            Bunch to select (default: -1, which means all particles)
        step : int, optional
            Step in H5 file (default: 0)
        turn : int, optional
            Turn of dataset (default: None, which implies no specific turn selection)
            (probe H5 files only)

        Returns
        -------
        float
            kurtosis

        Notes
        -----
        23. March 2018
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kurtosis.html
        """
        opal_logger.error('dask.stats.kurtosis does not agree with scipy.stats.kurtosis')
        data = self.selectData(var, **kwargs)

        return stats.kurtosis(data, axis=0, fisher=True).compute().item(0)


    def gaussian_kde(self, var, **kwargs):
        """Representation of a kernel-density estimate using Gaussian kernels.

        Parameters
        ----------
        var : str
            The variable
        bunch : int, optional
            Bunch to select (default: -1, which means all particles)
        step : int, optional
            Step in H5 file (default: 0)
        turn : int, optional
            Turn of dataset (default: None, which implies no specific turn selection)
            (probe H5 files only)

        Returns
        -------
        scipy.stats.gaussian_kde
            scipy kernel density estimator

        Notes
        -----
        23. March 2018
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.html
        """
        data = self.selectData(var, **kwargs)

        return dask.delayed(sc.stats.gaussian_kde)(data)


    def histogram(self, var, bins, range, **kwargs):
        """Compute a histogram of a dataset

        Parameters
        ----------
        var : str
            The variable
        bins : int or str
            Binning type or nr of bins
            (see https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.histogram.html)
        range : list
            Range of histogram
        bunch : int, optional
            Bunch to select (default: -1, which means all particles)
        step : int, optional
            Step in H5 file (default: 0)
        turn : int, optional
            Turn of dataset (default: None, which implies no specific turn selection)
            (probe H5 files only)
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
        density = kwargs.pop('density', True)

        data = self.selectData(var, **kwargs)

        return da.histogram(data, bins=bins, range=range, density=density)


    def halo_continuous_beam(self, var, **kwargs):
        r"""Compute the halo for a continuous beam.

        Compute the halo in horizontal or
        vertical direction according to

        .. math:: h_x = \frac{{<}x^4{>}} {{<}x^2{>}^2} - 2

        Parameters
        ----------
        var : str
            The variable
        bunch : int, optional
            Bunch to select (default: -1, which means all particles)
        step : int, optional
            Step in H5 file (default: 0)
        turn : int, optional
            Turn of dataset (default: None, which implies no specific turn selection)
            (probe H5 files only)

        Returns
        -------
        float
            halo

        References
        ----------
        T. P. Wangler, Los Alamos National Laboratory, Los Alamos, NM 87545,
        K. R. Crandall, TechSource, Santa Fe, NM 87594-1057,
        BEAM HALO IN PROTON LINAC BEAMS,
        XX International Linac Conference, Monterey, California
        """
        data = self.selectData(var, **kwargs)

        m4 = stats.moment(data, moment=4)
        m2 = stats.moment(data, moment=2)
        return (m4 / m2 ** 2 - 2.0).compute().item(0)


    def halo_ellipsoidal_beam(self, var, **kwargs):
        r"""Compute the halo for a ellipsoidal beam

        Compute the halo in horizontal, vertical
        or longitudinal direction according to

        .. math:: h_x = \frac{{<}x^4{>}} {{<}x^2{>}^2} - \frac{15}{7}

        Parameters
        ----------
        var : str
            The variable
        bunch : int, optional
            Bunch to select (default: -1, which means all particles)
        step : int, optional
            Step in H5 file (default: 0)
        turn : int, optional
            Turn of dataset (default: None, which implies no specific turn selection)
            (probe H5 files only)

        Returns
        -------
        float
            halo

        References
        ----------
        T. P. Wangler, Los Alamos National Laboratory, Los Alamos, NM 87545,
        K. R. Crandall, TechSource, Santa Fe, NM 87594-1057,
        BEAM HALO IN PROTON LINAC BEAMS,
        XX International Linac Conference, Monterey, California
        """
        data = self.selectData(var, **kwargs)

        m4 = stats.moment(data, moment=4)
        m2 = stats.moment(data, moment=2)

        return (m4 / m2 ** 2 - 15.0 / 7.0).compute().item(0)


    def radial_halo_ellipsoidal_beam(self, **kwargs):
        r"""Compute the radial halo for a ellipsoidal beam

        Compute the halo in radial direction
        according to

        .. math:: h_r = \frac{{<}r^4{>}} {{<}r^2{>}^2} - \frac{15}{7}

        Parameters
        ----------
        bunch : int, optional
            Bunch to select (default: -1, which means all particles)
        step : int, optional
            Step in H5 file (default: 0)
        turn : int, optional
            Turn of dataset (default: None, which implies no specific turn selection)
            (probe H5 files only)

        Returns
        -------
        float
            halo

        References
        ----------
        T. P. Wangler, Los Alamos National Laboratory, Los Alamos, NM 87545,
        K. R. Crandall, TechSource, Santa Fe, NM 87594-1057,
        BEAM HALO IN PROTON LINAC BEAMS,
        XX International Linac Conference, Monterey, California
        """
        x = self.selectData('x', **kwargs)
        y = self.selectData('y', **kwargs)

        r  = eval_radius(x, y)

        m4 = stats.moment(r, moment=4)
        m2 = stats.moment(r, moment=2)

        return (m4 / m2 ** 2 - 15.0 / 7.0).compute()


    def halo_2d_ellipsoidal_beam(self, var, **kwargs):
        r"""Compute the 2D halo for a ellipsoidal beam

        Compute the 2D halo in horizontal, vertical
        or longitudinal direction according to

        .. math::
            \begin{align}
            H_i & = \frac{\sqrt{3}} {2} \frac{\sqrt{A}} {B} - \frac{15}{7} \\
            A & = {<}q^4{>}{<}p^4{>} + 3 {<}q^2p^2{>}^2 - 4 {<}qp^3{>} {<}q^3p{>} \\
            B & = {<}q^2{>}{<}p^2{>} - {<}qp{>}^2
            \end{align}

        with coordinate q and momentum p. Specify either the
        'step' or 'turn' (probes only).

        Parameters
        ----------
        var : str
            The direction 'x', 'y', 'z'
        bunch : int, optional
            Bunch to select (default: -1, which means all particles)
        step : int, optional
            Step in H5 file (default: 0)
        turn : int, optional
            Turn of dataset (default: None, which implies no specific turn selection)
            (probe H5 files only)

        Returns
        -------
        float
            halo

        References
        ----------
        https://journals.aps.org/prab/abstract/10.1103/PhysRevSTAB.5.124202
        """
        q = self.selectData(var, **kwargs)
        p = self.selectData('p' + var, **kwargs)
        return self._halo_2d_ellipsoidal_beam(q, p)


    def radial_halo_2d_ellipsoidal_beam(self, azimuth, **kwargs):
        r"""Compute the 2D radial halo for a ellipsoidal beam

        Compute the 2D radial halo according to

        .. math::
            \begin{align}
            H_i & = \frac{\sqrt{3}}{2} \frac{\sqrt{A}}{B} - \frac{15}{7} \\
            A   & = {<}r^4{>}{<}p^4{>} + 3 {<}r^2p^2{>}^2 - 4 {<}rp^3{>} {<}r^3p{>} \\
            B   & = {<}r^2{>}{<}p^2{>} - {<}rp{>}^2
            \end{align}

        with radius r and radial momentum p.

        Parameters
        ----------
        azimuth : float
            Azimuth for radial halo only (in degree)
        bunch : int, optional
            Bunch to select (default: -1, which means all particles)
        step : int, optional
            Step in H5 file (default: 0)
        turn : int, optional
            Turn of dataset (default: None, which implies no specific turn selection)
            (probe H5 files only)

        Returns
        -------
        float
            halo

        References
        ----------
        https://journals.aps.org/prab/abstract/10.1103/PhysRevSTAB.5.124202
        """
        x = self.selectData('x', **kwargs)
        px = self.selectData('px', **kwargs)

        y = self.selectData('y', **kwargs)
        py = self.selectData('py', **kwargs)

        r  = eval_radius(x, y)

        azimuth = da.deg2rad(azimuth)

        pr = eval_radial_momentum(px, py, azimuth)

        return self._halo_2d_ellipsoidal_beam(r, pr)


    def _halo_2d_ellipsoidal_beam(self, q, p):
        r"""Compute the 2D halo

        Compute the 2D halo in horizontal, vertical
        or longitudinal direction according to

        .. math::
            \begin{align}
                H_i & = \frac{\sqrt{3}}{2} \frac{\sqrt{A}}{B} - \frac{15}{7} \\
                A & = {<}q^4{>}{<}p^4{>} + 3 {<}q^2p^2{>}^2 - 4 {<}qp^3{>} {<}q^3p{>} \\
                B & = {<}q^2{>}{<}p^2{>} - {<}qp{>}^2
            \end{align}

        with coordinate `q` and momentum `p`.

        Parameters
        ----------
        q : array_like
            coordinate data
        p : array_like
            momentum data

        Returns
        -------
        float
            halo

        References
        ----------
        https://journals.aps.org/prab/abstract/10.1103/PhysRevSTAB.5.124202
        """

        # make centered
        q = q - da.mean(q)
        p = p - da.mean(p)

        q2 = da.mean(q ** 2)
        q4 = da.mean(q ** 4)

        p2 = da.mean(p ** 2)
        p4 = da.mean(p ** 4)

        q1p1 = da.mean(q*p)
        q2p2 = da.mean(q**2 * p**2)
        q1p3 = da.mean(q * p**3)
        q3p1 = da.mean(q**3 * p)

        A = q4 * p4 + 3.0 * q2p2 ** 2 - 4.0 * q1p3 * q3p1
        B = q2 * p2 - q1p1 ** 2

        return (0.5 * da.sqrt(3.0 * A) / B - 15.0 / 7.0).compute()


    def projected_emittance(self, dim, **kwargs):
        r"""Compute the projected emittance

        It shifts the
        coordinates by their mean value such that the bunch
        is centered around zero.

        .. math:: \varepsilon = \sqrt{ {<}coords^2{>}{<}momenta^2{>} - {<}coords*momenta{>}^2 }

        Parameters
        ----------
        dim : str
            the dimension 'x', 'y' or 'z'

        Parameters
        ----------
        bunch : int, optional
            Bunch to select (default: -1, which means all particles)
        step : int, optional
            Step in H5 file (default: 0)
        turn : int, optional
            Turn of dataset (default: None, which implies no specific turn selection)
            (probe H5 files only)

        Returns
        -------
        float
            the projected emittance
        """
        coords  = self.selectData(dim, **kwargs)
        momenta = self.selectData('p' + dim, **kwargs)

        c2 = stats.moment(coords, moment=2)
        m2 = stats.moment(momenta, moment=2)

        # we need to shift coords to center the beam
        coords  -= coords.mean(axis=0)
        momenta -= momenta.mean(, axis=0)

        cm = (coords * momenta).mean(axis=0)

        return da.sqrt( m2 * c2 - cm ** 2 ).compute()


    def radial_projected_emittance(self, azimuth, **kwargs):
        r"""Compute the radial projected emittance

        It shifts the
        coordinates by their mean value such that the bunch
        is centered around zero.

        .. math:: \varepsilon = \sqrt{ {<}r^2{>}{<}p_r^2{>} - {<}r*p_r{>}^2 }

        Parameters
        ----------
        azimuth : float
            Azimuth angle (in degree)
        bunch : int, optional
            Bunch to select (default: -1, which means all particles)
        step : int, optional
            Step in H5 file (default: 0)
        turn : int, optional
            Turn of dataset (default: None, which implies no specific turn selection)
            (probe H5 files only)

        Returns
        -------
        float
            the projected emittance
        """
        x = self.selectData('x', **kwargs)
        px = self.selectData('px', **kwargs)

        y = self.selectData('y', **kwargs)
        py = self.selectData('py', **kwargs)

        r  = eval_radius(x, y)

        azimuth = np.deg2rad(azimuth)

        pr = eval_radial_momentum(px, py, azimuth)

        r2  = sc.stats.moment(r, moment=2)
        pr2 = sc.stats.moment(pr, moment=2)

        # we need to center the beam
        r  -= np.mean(r,  axis=0)
        pr -= np.mean(pr, axis=0)

        rpr = np.mean(r * pr, axis=0)

        return np.sqrt( r2 * pr2 - rpr ** 2 )


    def find_beams(self, var, **kwargs):
        """Compute the starting and end points of a beam via a histogram.

        The purpose of this script is to distinguish bunches
        of a multi-bunch simulation.

        Parameters
        ----------
        var : str
            The variable
        step : int, optional
            Step in H5 file (default: 0)
        bins : int, optional
            Number of bins for histogram (default: 0)
        Wn : float, optional
            Critical frequency for lowpass filter (default: 0.15)
            (see https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html)

        Returns
        -------
        peaks: ndarray
            Indices of minima locations
        hist : array
            The values of the corresponding numpy histogram.
        bin_edges : array of dtype float
            Return the bin edges ``(length(hist)+1)``.
        """
        step = kwargs.pop('step', 0)
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
        r"""Rotate the coordinates (`x`, `y`) by `theta` (degree)

        Parameters
        ----------
        x : dask.array
            x-data
        y : dask.array
            y-data
        theta : float
            The angle in degree

        Returns
        -------
        rx: dask.array
            rotated coordinates `x`
        ry: dask.array
            rotated coordinates `y`

        Notes
        -----
        .. math::
            \begin{align}
            R(\theta) & = \begin{bmatrix}
                           \cos(\theta) & -\sin(\theta) \\
                           \sin(\theta) &  \cos(\theta)
                        \end{bmatrix} \\
            \begin{bmatrix} rx & ry \end{bmatrix} & =
            R(\theta) * \begin{bmatrix} x & y \end{bmatrix}
            \end{align}

        References
        ----------
        https://en.wikipedia.org/wiki/Rotation_matrix
        """

        theta = da.deg2rad(theta)

        cos = da.cos(theta)
        sin = da.sin(theta)

        rx = x * cos - y * sin
        ry = x * sin + y * cos

        return rx, ry
