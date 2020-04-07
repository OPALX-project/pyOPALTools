def jupyter():
    """
    References
    ----------
    (8. April 2018)
    https://matplotlib.org/users/customizing.html
    """
    import matplotlib as mpl
    from cycler import cycler
    import opal.config as config
    from opal.utilities.logger import opal_logger

    # reset
    from opal.visualization.styles.default import default
    default()

    if mpl.__version__ < '2':
        opal_logger.error('jupyter style not available for matplotlib version ' + mpl.__version__)

    config.opal['style'] = 'jupyter'

    mpl.rcParams['axes.autolimit_mode']             = 'data'
    mpl.rcParams['axes.axisbelow']                  = 'line'
    mpl.rcParams['axes.edgecolor']                  = 'k'
    mpl.rcParams['axes.facecolor']                  = 'w'
    mpl.rcParams['axes.formatter.limits']           = [-7, 7]

    if mpl.__version__ >= '2.1':
        mpl.rcParams['axes.formatter.min_exponent'] = 0

    mpl.rcParams['axes.formatter.offset_threshold'] = 4
    mpl.rcParams['axes.formatter.use_locale']       = False
    mpl.rcParams['axes.formatter.use_mathtext']     = False
    mpl.rcParams['axes.formatter.useoffset']        = True
    mpl.rcParams['axes.grid']                       = False
    mpl.rcParams['axes.grid.axis']                  = 'both'
    mpl.rcParams['axes.grid.which']                 = 'both'
    # axis.hold deprecated in version 2 and removed in version 3
    if mpl.__version__ < '3':
        mpl.rcParams['axes.hold']                       = None

    mpl.rcParams['axes.labelcolor']                 = 'k'
    mpl.rcParams['axes.labelpad']                   = 4.0
    mpl.rcParams['axes.labelsize']                  = 'medium'
    mpl.rcParams['axes.labelweight']                = 'normal'
    mpl.rcParams['axes.linewidth']                  = 0.8
    mpl.rcParams['axes.prop_cycle']                 = cycler('color', ['#1f77b4',
                                                                    '#ff7f0e',
                                                                    '#2ca02c',
                                                                    '#d62728',
                                                                    '#9467bd',
                                                                    '#8c564b',
                                                                    '#e377c2',
                                                                    '#7f7f7f',
                                                                    '#bcbd22',
                                                                    '#17becf'])
    mpl.rcParams['axes.spines.bottom']              = True
    mpl.rcParams['axes.spines.left']                = True
    mpl.rcParams['axes.spines.right']               = False
    mpl.rcParams['axes.spines.top']                 = False
    mpl.rcParams['axes.titlepad']                   = 6.0
    mpl.rcParams['axes.titlesize']                  = 'large'
    mpl.rcParams['axes.titleweight']                = 'normal'
    mpl.rcParams['axes.unicode_minus']              = True
    mpl.rcParams['axes.xmargin']                    = 0.05
    mpl.rcParams['axes.ymargin']                    = 0.05
    mpl.rcParams['axes3d.grid']                     = True

    mpl.rcParams['savefig.dpi']             = 300

    mpl.rcParams['figure.autolayout']       = False             # When True, automatically adjust subplot
                                                                # parameters to make the plot fit the figure
    mpl.rcParams['figure.edgecolor']        = (1, 1, 1, 0)
    mpl.rcParams['figure.facecolor']        = (1, 1, 1, 0)
    mpl.rcParams['figure.figsize']          = [12.0, 7.0]       # figure size in inches
    mpl.rcParams['figure.dpi']              = 300               # figure dots per inch
    mpl.rcParams['figure.frameon']          = True
    mpl.rcParams['figure.max_open_warning'] = 20
    mpl.rcParams['figure.subplot.bottom']   = 0.125
    mpl.rcParams['figure.subplot.hspace']   = 0.2
    mpl.rcParams['figure.subplot.left']     = 0.125
    mpl.rcParams['figure.subplot.right']    = 0.9
    mpl.rcParams['figure.subplot.top']      = 0.88
    mpl.rcParams['figure.subplot.wspace']   = 0.2
    mpl.rcParams['figure.titlesize']        = 'large'           # size of the figure title (Figure.suptitle())
    mpl.rcParams['figure.titleweight']      = 'normal'          # weight of the figure title

    mpl.rcParams['font.family']             = 'serif'
    mpl.rcParams['font.size']               = 18
    mpl.rcParams['font.stretch']            = 'normal'
    mpl.rcParams['font.style']              = 'normal'
    mpl.rcParams['font.variant']            = 'normal'
    mpl.rcParams['font.weight']             = 'normal'


    mpl.rcParams['grid.color']              = 'b0b0b0'
    mpl.rcParams['grid.linestyle']          = '-'
    mpl.rcParams['grid.linewidth']          = 0.8
    mpl.rcParams['grid.alpha']              = 1.0


    mpl.rcParams['legend.borderaxespad']    = 0.5
    mpl.rcParams['legend.borderpad']        = 0.4
    mpl.rcParams['legend.columnspacing']    = 2.0
    mpl.rcParams['legend.edgecolor']        = 'inherit'
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

    # 1. April 2019
    # https://stackoverflow.com/questions/40894859/how-do-i-check-from-within-python-whether-latex-and-tex-live-are-installed-on-a
    from distutils.spawn import find_executable
    if find_executable('latex'):
        mpl.rcParams['text.usetex']         = True
    else:
        mpl.rcParams['text.usetex']         = False

    mpl.rcParams['xtick.alignment']         = 'center'
    mpl.rcParams['xtick.bottom']            = True
    mpl.rcParams['xtick.color']             = 'k'
    mpl.rcParams['xtick.direction']         = 'out'
    mpl.rcParams['xtick.labelsize']         = 'medium'
    mpl.rcParams['xtick.major.bottom']      = True
    mpl.rcParams['xtick.major.pad']         = 3.5
    mpl.rcParams['xtick.major.size']        = 3.5
    mpl.rcParams['xtick.major.top']         = True
    mpl.rcParams['xtick.major.width']       = 0.8
    mpl.rcParams['xtick.minor.bottom']      = True
    mpl.rcParams['xtick.minor.pad']         = 3.4
    mpl.rcParams['xtick.minor.size']        = 2.0
    mpl.rcParams['xtick.minor.top']         = True
    mpl.rcParams['xtick.minor.visible']     = False
    mpl.rcParams['xtick.minor.width']       = 0.6
    mpl.rcParams['xtick.top']               = False

    mpl.rcParams['ytick.alignment']         = 'center_baseline'
    mpl.rcParams['ytick.color']             = 'k'
    mpl.rcParams['ytick.direction']         = 'out'
    mpl.rcParams['ytick.labelsize']         = 'medium'
    mpl.rcParams['ytick.left']              = True
    mpl.rcParams['ytick.major.left']        = True
    mpl.rcParams['ytick.major.pad']         = 3.5
    mpl.rcParams['ytick.major.right']       = True
    mpl.rcParams['ytick.major.size']        = 3.5
    mpl.rcParams['ytick.major.width']       = 0.8
    mpl.rcParams['ytick.minor.left']        = True
    mpl.rcParams['ytick.minor.pad']         = 3.4
    mpl.rcParams['ytick.minor.right']       = True
    mpl.rcParams['ytick.minor.size']        = 2.0
    mpl.rcParams['ytick.minor.visible']     = False
    mpl.rcParams['ytick.minor.width']       = 0.6
    mpl.rcParams['ytick.right']             = False


    try:
        from plotly import offline
        offline.init_notebook_mode(connected=True)
    except:
        opal_logger.error('Install plotly: pip install plotly')
