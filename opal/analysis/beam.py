# Author:   Matthias Frey
# Date:     March 2018

from opal.statistics import statistics as stat

def halo_continuous_beam(ds, var, , **kwargs):
    """
    Compute the halo in horizontal or
    vertical direction according to
    
    h_x = <x^4> / <x^2>^2 - 2
    
    Reference
    ---------
    T. P. Wangler, Los Alamos National Laboratory, Los Alamos, NM 87545,
    K. R. Crandall, TechSource, Santa Fe, NM 87594-1057,
    BEAM HALO IN PROTON LINAC BEAMS,
    XX International Linac Conference, Monterey, California
    """
    m4 = stat.moment(ds, var, k=4, **kwargs)
    m2 = stat.moment(ds, var, k=2, **kwargs)
    
    return m4 / m2 ** 2 - 2.0


def halo_ellipsoidal_beam(ds, var):
    """
    Compute the halo in horizontal, vertical
    or longitudinal direction according to
    
    h_x = <x^4> / <x^2>^2 - 15 / 17
    
    Reference
    ---------
    T. P. Wangler, Los Alamos National Laboratory, Los Alamos, NM 87545,
    K. R. Crandall, TechSource, Santa Fe, NM 87594-1057,
    BEAM HALO IN PROTON LINAC BEAMS,
    XX International Linac Conference, Monterey, California
    """
    m4 = stat.moment(ds, var, k=4, **kwargs)
    m2 = stat.moment(ds, var, k=2, **kwargs)
    
    return m4 / m2 ** 2 - 15.0 / 17.0
