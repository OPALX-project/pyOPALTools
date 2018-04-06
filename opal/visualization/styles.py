import matplotlib as mpl


# https://matplotlib.org/users/dflt_style_changes.html

def default_style():
    mpl.rcParams['figure.figsize'] = [7.0, 6.0]
    mpl.rcParams['figure.dpi'] = 100
    mpl.rcParams['savefig.dpi'] = 300
    
    mpl.rcParams['font.size'] = 12
    mpl.rcParams['legend.fontsize'] = 'large'
    mpl.rcParams['figure.titlesize'] = 'medium'


def jupyter_style():
    mpl.rcParams['figure.figsize'] = [7.0, 5.0]
    mpl.rcParams['figure.dpi'] = 300
    mpl.rcParams['savefig.dpi'] = 300
    
    mpl.rcParams['font.size'] = 10
    mpl.rcParams['legend.fontsize'] = 'medium'
    mpl.rcParams['figure.titlesize'] = 'medium'
