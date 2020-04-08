# Copyright (c) 2019, Matthias Frey, Paul Scherrer Institut, Villigen PSI, Switzerland
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

def poster():
    """
    References
    ----------
    (8. April 2018)
    https://matplotlib.org/users/customizing.html
    """
    import matplotlib as mpl
    import opal.config as config
    from . import jupyter

    config.opal['style'] = 'poster'

    mpl.rcParams['figure.figsize']      = [18.0, 13.0]       # figure size in inches
    mpl.rcParams['axes.labelsize']      = 'xx-large'
    mpl.rcParams['axes.linewidth']      = 3.0
    mpl.rcParams['font.size']           = 22.0
    mpl.rcParams['legend.fontsize']     = 'x-large'
    mpl.rcParams['xtick.labelsize']     = 'xx-large'
    mpl.rcParams['ytick.labelsize']     = 'xx-large'
    mpl.rcParams['xtick.major.width']   = 3
    mpl.rcParams['xtick.minor.width']   = 1.5
    mpl.rcParams['ytick.major.width']   = 3
    mpl.rcParams['ytick.minor.width']   = 1.5
    mpl.rcParams['lines.linewidth']     = 7.0
    mpl.rcParams['grid.linewidth']      = 2.5
