# Author:   Matthias Frey
# Date:     March 2018

from opal.statistics import statistics as stat
from opal.datasets.DatasetBase import DatasetBase, FileType
from opal.analysis import impl_beam
import numpy as np

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
    step    (int)           of dataset
    bin     (int)           energy bin for which to compute
    
    Reference
    ---------
    T. P. Wangler, Los Alamos National Laboratory, Los Alamos, NM 87545,
    K. R. Crandall, TechSource, Santa Fe, NM 87594-1057,
    BEAM HALO IN PROTON LINAC BEAMS,
    XX International Linac Conference, Monterey, California
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    step = kwargs.get('step', 0)
    
    data = ds.getData(var, step=step)
    
    energy_bin = kwargs.get('bin', -1)
    if energy_bin > 0 and ds.filetype == FileType.H5:
        bins = ds.getData('bin', step=step)
        data = data[np.where(bins == energy_bin)]
    
    return impl_beam.halo_continuous_beam(data)


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
    step    (int)           of dataset
    bin     (int)           energy bin for which to compute
    
    Reference
    ---------
    T. P. Wangler, Los Alamos National Laboratory, Los Alamos, NM 87545,
    K. R. Crandall, TechSource, Santa Fe, NM 87594-1057,
    BEAM HALO IN PROTON LINAC BEAMS,
    XX International Linac Conference, Monterey, California
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    step = kwargs.get('step', 0)
    
    data = ds.getData(var, step=step)
    
    energy_bin = kwargs.get('bin', -1)
    if energy_bin > 0 and ds.filetype == FileType.H5:
        bins = ds.getData('bin', step=step)
        data = data[np.where(bins == energy_bin)]
    
    return impl_beam.halo_ellipsoidal_beam(data)


def projected_emittance(ds, dim, **kwargs):
    """
    Compute the projected emittance. It shifts the
    coordinates by their mean value such that the bunch
    is centered around zero.
    
    \varepsilon = \sqrt{ <coords^2><momenta^2> - <coords*momenta>^2 }
    
    Parameters
    ----------
    ds      (DatasetBase)   datasets
    dim     (str)           the dimension 'x', 'y' or 'z'
    
    Optionals
    ---------
    step    (int)           of dataset
    bin     (int)           energy bin for which to compute
    
    Returns
    -------
    the projected emittance
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    step = kwargs.get('step', 0)
    
    coords = ds.getData(dim, step=step)
    momenta = ds.getData('p' + dim, step=step)
    
    energy_bin = kwargs.get('bin', -1)
    if energy_bin > 0 and ds.filetype == FileType.H5:
        bins = ds.getData('bin', step=step)
        coords = coords[np.where(bins == energy_bin)]
        momenta = momenta[np.where(bins == energy_bin)]
    
    return impl_beam.projected_emittance(coords, momenta)


def find_beams(ds, var, **kwargs):
    """
    Compute the starting and end points of a beam via
    a histogram.
    The purpose of this script is to distinguish bunches
    of a multi-bunch simulation.
    
    Parameters
    ----------
    ds      (DatasetBase)   datasets
    var     (str)           the variable
    
    Optionals
    ---------
    step    (int)           of dataset
    bins    (int)           number of bins for histogram
    
    Returns
    -------
    a list of minima locations and corresponding histogram
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    step    = kwargs.get('step', 0)
    
    data = ds.getData(var, step=step)
    
    return impl_beam.find_beams(data, **kwargs)


def get_beam(ds, var, k, **kwargs):
    """
    Obtain the data of a variable of a beam in a
    multi-bunch simulation.
    
    Parameters
    ----------
    ds      (DatasetBase)   datasets
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
    
    indices, hist = get_beam_indices(ds, k, **kwargs)
    
    step    = kwargs.get('step', 0)
    
    data = ds.getData(var, step=step)
    
    return data[indices], hist
    

def get_beam_indices(ds, k, **kwargs):
    """
    Obtain the indices of the data that belongs to the
    selected beam. Use in multi-bunch simulation data.
    
    Parameters
    ----------
    ds      (DatasetBase)   datasets
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
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.H5:
        raise TypeError(ds.filename + ' is not a H5 dataset.')
    
    if k < 0:
        raise ValueError("Bunch number has to be 'k >= 0'.")
    
    step    = kwargs.get('step', 0)
    
    # opal-t vs. opal-cycl
    opal_flavour = ds.getData('flavour')[step]
    
    if opal_flavour == 'opal-cycl':
        xdata = ds.getData('x', step=step)
        ydata = ds.getData('y', step=step)
        
        # rotate beam around (0, 0) such that it's horizontal
        # --> we can do histogram independent of azimuth (dumping angle)
        azimuth = ds.getData('AZIMUTH')[step]
        
        #if ds.getUnit('REFAZIMUTH') == 'rad':
            #azimuth = np.rad2deg(azimuth)
        
        xdata, _ = impl_beam.rotate(xdata, ydata, -azimuth)
        
        minima, hist = impl_beam.find_beams(xdata, **kwargs)
        
    else:
        raise ValueError("Only implemented for OPAL-CYCL.")
    
    if k > len(minima) - 1:
        raise ValueError("Bunch number has to be 'k < " + str(len(minima)) + "'.")
    
    xdata = np.asarray(xdata)
    
    if k == len(minima):
        # last bunch includes particles from upper part [k, k+1]
        return ((xdata >= minima[k]) & (xdata <= minima[k+1])), hist
    else:
        # do not include upper part [k, k+1[
        return ((xdata >= minima[k]) & (xdata < minima[k+1])), hist
