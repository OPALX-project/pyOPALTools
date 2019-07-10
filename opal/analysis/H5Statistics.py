from opal.analysis.Statistics import Statistics
from opal.analysis import impl_beam
import dask.array as da
from dask.array import stats

class H5Statistics(Statistics):

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
        step = kwargs.pop('step', 0)
        
        data = self.ds.getData(var, step=step)
        
        bunch = kwargs.pop('bunch', 0)
        if bunch > -1:
            bunchnum = self.ds.getData('bunchNumber', step=step)
            da.compress(bunch == bunchnum, data)

        return stats.moment(data, axis=0, moment=k)


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
        step = kwargs.pop('step', 0)
        
        data = self.ds.getData(var, step=step)
        
        bunch = kwargs.pop('bunch', 0)
        if bunch > -1:
            bunchnum = self.ds.getData('bunchNumber', step=step)
            data = da.compress(bunch == bunchnum, data)
            
        return data.mean(axis=0)


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
        step = kwargs.pop('step', 0)
        
        data = self.ds.getData(var, step=step)
        
        bunch = kwargs.pop('bunch', 0)
        if bunch > -1:
            bunchnum = self.ds.getData('bunchNumber', step=step)
            data = da.compress(bunch == bunchnum, data)
        
        return stats.skew(data, axis=0)


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
        step = kwargs.pop('step', 0)
        
        data = self.ds.getData(var, step=step)
        
        bunch = kwargs.pop('bunch', 0)
        if bunch > -1:
            bunchnum = self.ds.getData('bunchNumber', step=step)
            data = da.compress(bunch == bunchnum, data)
        
        return stats.kurtosis(data, axis=0, fisher=True)


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
        bins    = kwargs.pop('bins', 'sturges')
        density = kwargs.pop('density', True)
        
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
        data = self.ds.getData(var, step=step)
        
        bunch = kwargs.pop('bunch', 0)
        if bunch > -1:
            bunchnum = self.ds.getData('bunchNumber', step=step)
            data = da.compress(bunch == bunchnum, data)

        return impl_beam.halo_continuous_beam(data)


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
        
        data = self.ds.getData(var, step=step)
        
        bunch = kwargs.pop('bunch', 0)
        if bunch > -1:
            bunchnum = self.ds.getData('bunchNumber', step=step)
            data = da.compress(bunch == bunchnum, data)
        return impl_beam.halo_ellipsoidal_beam(data)


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
        
        bunch = kwargs.pop('bunch', 0)
        if bunch > -1:
            bunchnum = self.ds.getData('bunchNumber', step=step)
            coords = da.compress(bunch == bunchnum, coords)
            momenta = da.compress(bunch == bunchnum, momenta)

        return impl_beam.projected_emittance(coords, momenta)


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
        step    = kwargs.pop('step', 0)
        
        data = self.ds.getData(var, step=step)
        
        return impl_beam.find_beams(data, **kwargs)


    def get_beam(self, var, k, **kwargs):
        """
        Obtain the data of a variable of a beam in a
        multi-bunch simulation.
        
        Parameters
        ----------
        var     (str)           the variable
        k       (int)           select k-th bunch
        
        Optionals
        ---------
        step    (int)           of dataset
        bins    (int)           number of bins for histogram
        
        Returns
        -------
        the data as an array / list + histogram to find bunch
        """
        
        indices, hist = self.get_beam_indices(k, **kwargs)
        
        step    = kwargs.pop('step', 0)
        
        data = self.ds.getData(var, step=step)
        
        return da.compress(indices, data), hist
        

    def get_beam_indices(self, k, **kwargs):
        """
        Obtain the indices of the data that belongs to the
        selected beam. Use in multi-bunch simulation data.
        
        Parameters
        ----------
        k       (int)           select k-th bunch
        
        Optionals
        ---------
        step    (int)           of dataset
        bins    (int)           number of bins for histogram
        
        Returns
        -------
        an array containing booleans. An entry is
        true if appropriate data belongs to **this** bunch.
        The 'True' entries can be exracted from a data array
        using numpy.extract.
        It returns also the histogram.
        
        References
        ----------
        https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.extract.html
        """
        if k < 0:
            raise ValueError("Bunch number has to be 'k >= 0'.")
        
        step    = kwargs.pop('step', 0)
        
        # opal-t vs. opal-cycl
        opal_flavour = self.ds.getData('flavour')[step]
        
        if opal_flavour == 'opal-cycl':
            xdata = self.ds.getData('x', step=step)
            ydata = self.ds.getData('y', step=step)
            
            # rotate beam around (0, 0) such that it's horizontal
            # --> we can do histogram independent of azimuth (dumping angle)
            azimuth = self.ds.getData('AZIMUTH')[step]
            
            #if self.ds.getUnit('REFAZIMUTH') == 'rad':
                #azimuth = np.rad2deg(azimuth)
            
            xdata, _ = impl_beam.rotate(xdata, ydata, -azimuth)
            
            minima, hist = impl_beam.find_beams(xdata, **kwargs)
            
        else:
            raise ValueError("Only implemented for OPAL-CYCL.")
        
        if k > len(minima) - 1:
            raise ValueError("Bunch number has to be 'k < " + str(len(minima)) + "'.")
        
        if k == len(minima):
            # last bunch includes particles from upper part [k, k+1]
            return da.compress((xdata >= minima[k]) & (xdata <= minima[k+1]), xdata), hist
        else:
            # do not include upper part [k, k+1[
            return da.compress((xdata >= minima[k]) & (xdata < minima[k+1]), xdata), hist
