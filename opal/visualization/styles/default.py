"""
Reference (8. April 2018)
---------
https://matplotlib.org/users/customizing.html
"""
# https://matplotlib.org/users/dflt_style_changes.html
import matplotlib as mpl
import opal.config as config

config.opal['style'] = 'default'

mpl.rcParams['figure.figsize']          = [7.0, 6.0]
mpl.rcParams['figure.dpi']              = 100
mpl.rcParams['savefig.dpi']             = 300

mpl.rcParams['font.size']               = 12
mpl.rcParams['legend.fontsize']         = 'large'
mpl.rcParams['figure.titlesize']        = 'medium'
