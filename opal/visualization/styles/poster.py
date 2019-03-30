"""
Reference (8. April 2018)
---------
https://matplotlib.org/users/customizing.html
"""
import matplotlib as mpl
import opal.config as config
from . import jupyter

config.opal['style'] = 'poster'

mpl.rcParams['figure.figsize']  = [18.0, 13.0]       # figure size in inches
mpl.rcParams['axes.labelsize']  = 'xx-large'
mpl.rcParams['axes.linewidth']  = 3.0
mpl.rcParams['font.size']       = 22.0
mpl.rcParams['legend.fontsize'] = 'x-large'
mpl.rcParams['xtick.labelsize'] = 'xx-large'
mpl.rcParams['ytick.labelsize'] = 'xx-large'
mpl.rcParams['lines.linewidth'] = 7.0
mpl.rcParams['grid.linewidth']  = 2.5
