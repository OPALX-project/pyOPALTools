import matplotlib as mpl


# https://matplotlib.org/users/dflt_style_changes.html

def default_style():
    mpl.rcParams['figure.figsize']          = [7.0, 6.0]
    mpl.rcParams['figure.dpi']              = 100
    mpl.rcParams['savefig.dpi']             = 300
    
    mpl.rcParams['font.size']               = 12
    mpl.rcParams['legend.fontsize']         = 'large'
    mpl.rcParams['figure.titlesize']        = 'medium'


def jupyter_style():
    mpl.rcParams['savefig.dpi']             = 300
    
    mpl.rcParams['figure.autolayout']       = False
    mpl.rcParams['figure.edgecolor']        = (1, 1, 1, 0)
    mpl.rcParams['figure.facecolor']        = (1, 1, 1, 0)
    mpl.rcParams['figure.figsize']          = [12.0, 7.0]
    mpl.rcParams['figure.dpi']              = 300
    mpl.rcParams['figure.frameon']          = True
    mpl.rcParams['figure.max_open_warning'] = 20
    mpl.rcParams['figure.subplot.bottom']   = 0.125
    mpl.rcParams['figure.subplot.hspace']   = 0.2
    mpl.rcParams['figure.subplot.left']     = 0.125
    mpl.rcParams['figure.subplot.right']    = 0.9
    mpl.rcParams['figure.subplot.top']      = 0.88
    mpl.rcParams['figure.subplot.wspace']   = 0.2
    mpl.rcParams['figure.titlesize']        = 'large'
    mpl.rcParams['figure.titleweight']      = 'normal'
    
    mpl.rcParams['font.size']               = 10.0
    mpl.rcParams['font.stretch']            = 'normal'
    mpl.rcParams['font.style']              = 'normal'
    mpl.rcParams['font.variant']            = 'normal'
    mpl.rcParams['font.weight']             = 'normal'
    
    
    mpl.rcParams['legend.borderaxespad']    = 0.5
    mpl.rcParams['legend.borderpad']        = 0.4
    mpl.rcParams['legend.columnspacing']    = 2.0
    #mpl.rcParams['legend.edgecolor']        = 0.8
    mpl.rcParams['legend.facecolor']        = 'inherit'
    mpl.rcParams['legend.fancybox']         = True
    mpl.rcParams['legend.fontsize']         = 'medium'
    mpl.rcParams['legend.framealpha']       = 0.8
    mpl.rcParams['legend.frameon']          = True
    mpl.rcParams['legend.handleheight']     = 0.7
    mpl.rcParams['legend.handlelength']     = 2.0
    mpl.rcParams['legend.handletextpad']    = 0.8
    mpl.rcParams['legend.labelspacing']     = 0.5
    mpl.rcParams['legend.loc']              = 'best'
    mpl.rcParams['legend.markerscale']      = 1.0
    mpl.rcParams['legend.numpoints']        = 1
    mpl.rcParams['legend.scatterpoints']    = 1
    mpl.rcParams['legend.shadow']           = False
