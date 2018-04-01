# Author:   Matthias Frey
# Date:     March 2018

from opal.statistics import statistics as stat
from opal.datasets.DatasetBase import DatasetBase
from opal.analysis import impl_beam

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


def find_beams(ds, var, **kwargs):
    """
    Compute the starting and end points of a beam via
    kernel density estimation and the calculation of
    relative minima of the dataset.
    The purpose of this script is to distinguish bunches
    of a multi-bunch simulation.
    
    Parameters
    ----------
    ds      (DatasetBase)   datasets
    var     (str)           the variable
    
    Optionals
    ---------
    step    (int)           of dataset
    npoints (int)           number of points to evaluate
                            kernel density estimator
    
    Returns
    -------
    a list of minima locations
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
    npoints (int)           number of points to evaluate
                            kernel density estimator
    
    Returns
    -------
    the data as an array / list
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if k < 0:
        raise ValueError("Bunch number has to be 'k >= 0'.")
    
    step    = kwargs.get('step', 0)
    
    data = ds.getData(var, step=step)
    
    minima = impl_beam.find_beams(data, **kwargs)
    
    if k > len(minima) - 1:
        raise ValueError("Bunch number has to be 'k < " + str(len(minima)) + "'.")
    
    # 1. April 2018
    # https://stackoverflow.com/questions/16343752/numpy-where-function-multiple-conditions
    if k == len(minima):
        # last bunch includes particles from upper part [k, k+1]
        return data[(data >= minima[k]) & (data <= minima[k+1])]
    else:
        # do not include upper part [k, k+1[
        return data[(data >= minima[k]) & (data < minima[k+1])]
