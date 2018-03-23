import numpy as np
import scipy as sc

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
    
    data = ds.getData(var)
    
    energy_bin = kwargs.get('bin', -1)
    if energy_bin > 0 and ds.ftype == FileType.H5:
        bins = ds.getData('bin')
        data = data[np.where(bins > energy_bin)]
    
    return sc.stats.moment(data, axis=0, moment=k)
    