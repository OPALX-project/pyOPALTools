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

def default():
    """
    References
    ----------
    (8. April 2018)
    https://matplotlib.org/users/customizing.html
    """
    # https://matplotlib.org/users/dflt_style_changes.html
    import matplotlib as mpl
    import opal.config as config

    config.opal['style'] = 'default'

    # Modified version of MATPLOTLIBRC FORMAT

    ### LINES
    # See http://matplotlib.org/api/artist_api.html#module-matplotlib.lines for more
    # information on line properties.
    mpl.rcParams['lines.linewidth']         = '1.5'         # line width in points
    mpl.rcParams['lines.linestyle']         = '-'           # solid line
    mpl.rcParams['lines.color']             = 'C0'          # has no affect on plot(); see axes.prop_cycle
    mpl.rcParams['lines.marker']            = None          # the default marker
    mpl.rcParams['lines.markeredgewidth']   = 1.0           # the line width around the marker symbol
    mpl.rcParams['lines.markersize']        = 6             # markersize, in points
    mpl.rcParams['lines.dash_joinstyle']    = 'miter'       # miter|round|bevel
    mpl.rcParams['lines.dash_capstyle']     = 'butt'        # butt|round|projecting
    mpl.rcParams['lines.solid_joinstyle']   = 'miter'       # miter|round|bevel
    mpl.rcParams['lines.solid_capstyle']    = 'projecting'  # butt|round|projecting
    mpl.rcParams['lines.antialiased']       = True          # render lines in antialiased (no jaggies)

    # The three standard dash patterns.  These are scaled by the linewidth.
    mpl.rcParams['lines.dashed_pattern']    = 2.8, 1.2
    mpl.rcParams['lines.dashdot_pattern']   = 4.8, 1.2, 0.8, 1.2
    mpl.rcParams['lines.dotted_pattern']    = 1.1, 1.1
    mpl.rcParams['lines.scale_dashes']      = True

    mpl.rcParams['markers.fillstyle']       = 'full'        # full|left|right|bottom|top|none

    ### PATCHES
    # Patches are graphical objects that fill 2D space, like polygons or
    # circles.  See
    # http://matplotlib.org/api/artist_api.html#module-matplotlib.patches
    # information on patch properties
    mpl.rcParams['patch.linewidth']         = 1        # edge width in points.
    mpl.rcParams['patch.facecolor']         = 'C0'
    mpl.rcParams['patch.edgecolor']         = 'black'   # if forced, or patch is not filled
    mpl.rcParams['patch.force_edgecolor']   = False   # True to always use edgecolor
    mpl.rcParams['patch.antialiased']       = True    # render patches in antialiased (no jaggies)

    ### HATCHES
    mpl.rcParams['hatch.color']     = 'k'
    mpl.rcParams['hatch.linewidth'] = 1.0

    ### Boxplot
    mpl.rcParams['boxplot.notch']       = False
    mpl.rcParams['boxplot.vertical']    = True
    mpl.rcParams['boxplot.whiskers']    = 1.5
    mpl.rcParams['boxplot.bootstrap']   = None
    mpl.rcParams['boxplot.patchartist'] = False
    mpl.rcParams['boxplot.showmeans']   = False
    mpl.rcParams['boxplot.showcaps']    = True
    mpl.rcParams['boxplot.showbox']     = True
    mpl.rcParams['boxplot.showfliers']  = True
    mpl.rcParams['boxplot.meanline']    = False

    mpl.rcParams['boxplot.flierprops.color']           = 'k'
    mpl.rcParams['boxplot.flierprops.marker']          = 'o'
    mpl.rcParams['boxplot.flierprops.markerfacecolor'] = 'none'
    mpl.rcParams['boxplot.flierprops.markeredgecolor'] = 'k'
    mpl.rcParams['boxplot.flierprops.markersize']      = 6
    mpl.rcParams['boxplot.flierprops.linestyle']       = 'none'
    mpl.rcParams['boxplot.flierprops.linewidth']       = 1.0

    mpl.rcParams['boxplot.boxprops.color']     = 'k'
    mpl.rcParams['boxplot.boxprops.linewidth'] = 1.0
    mpl.rcParams['boxplot.boxprops.linestyle'] = '-'

    mpl.rcParams['boxplot.whiskerprops.color']     = 'k'
    mpl.rcParams['boxplot.whiskerprops.linewidth'] = 1.0
    mpl.rcParams['boxplot.whiskerprops.linestyle'] = '-'

    mpl.rcParams['boxplot.capprops.color']     = 'k'
    mpl.rcParams['boxplot.capprops.linewidth'] = 1.0
    mpl.rcParams['boxplot.capprops.linestyle'] = '-'

    mpl.rcParams['boxplot.medianprops.color']     = 'C1'
    mpl.rcParams['boxplot.medianprops.linewidth'] = 1.0
    mpl.rcParams['boxplot.medianprops.linestyle'] = '-'

    mpl.rcParams['boxplot.meanprops.color']           = 'C2'
    mpl.rcParams['boxplot.meanprops.marker']          = '^'
    mpl.rcParams['boxplot.meanprops.markerfacecolor'] = 'C2'
    mpl.rcParams['boxplot.meanprops.markeredgecolor'] = 'C2'
    mpl.rcParams['boxplot.meanprops.markersize']      =  6
    mpl.rcParams['boxplot.meanprops.linestyle']       = 'none'
    mpl.rcParams['boxplot.meanprops.linewidth']       = 1.0

    ### FONT
    mpl.rcParams['font.family']         = 'sans-serif'
    mpl.rcParams['font.style']          = 'normal'
    mpl.rcParams['font.variant']        = 'normal'
    mpl.rcParams['font.weight']         = 'medium'
    mpl.rcParams['font.stretch']        = 'normal'

    ### TEXT
    # text properties used by text.Text.  See
    # http://matplotlib.org/api/artist_api.html#module-matplotlib.text for more
    # information on text properties

    mpl.rcParams['text.color']          = 'black'

    ### LaTeX customizations. See http://wiki.scipy.org/Cookbook/Matplotlib/UsingTex
    # use latex for all text handling. The following fonts
    # are supported through the usual rc parameter settings:
    # new century schoolbook, bookman, times, palatino,
    # zapf chancery, charter, serif, sans-serif, helvetica,
    # avant garde, courier, monospace, computer modern roman,
    # computer modern sans serif, computer modern typewriter
    # If another font is desired which can loaded using the
    # LaTeX \usepackage command, please inquire at the
    # matplotlib mailing list
    mpl.rcParams['text.usetex']         = False

    # use "ucs" and "inputenc" LaTeX packages for handling
    # unicode strings.
    if mpl.__version__ < '2.2':
        mpl.rcParams['text.latex.unicode'] = False

    # May be one of the following:
    #   'none': Perform no hinting
    #   'auto': Use FreeType's autohinter
    #   'native': Use the hinting information in the
    #             font file, if available, and if your
    #             FreeType library supports it
    #   'either': Use the native hinting information,
    #             or the autohinter if none is available.
    # For backward compatibility, this value may also be
    # True === 'auto' or False === 'none'.
    mpl.rcParams['text.hinting'] = 'auto'

    # Specifies the amount of softness for hinting in the
    # horizontal direction.  A value of 1 will hint to full
    # pixels.  A value of 2 will hint to half pixels etc.
    mpl.rcParams['text.hinting_factor'] = 8

    # If True (default), the text will be antialiased.
    # This only affects the Agg backend.
    mpl.rcParams['text.antialiased'] = True

    # The following settings allow you to select the fonts in math mode.
    # They map from a TeX font name to a fontconfig font pattern.
    # These settings are only used if mathtext.fontset is 'custom'.
    # Note that this "custom" mode is unsupported and may go away in the
    # future.
    mpl.rcParams['mathtext.cal'] = 'cursive'
    mpl.rcParams['mathtext.rm']  = 'serif'
    mpl.rcParams['mathtext.tt']  = 'monospace'
    mpl.rcParams['mathtext.it']  = 'serif:italic'
    mpl.rcParams['mathtext.bf']  = 'serif:bold'
    mpl.rcParams['mathtext.sf']  = 'sans'

    # Should be 'dejavusans' (default),
    # 'dejavuserif', 'cm' (Computer Modern), 'stix',
    # 'stixsans' or 'custom'
    mpl.rcParams['mathtext.fontset'] = 'dejavusans'

    # When True, use symbols from the Computer Modern
    # fonts when a symbol can not be found in one of
    # the custom math fonts.
    mpl.rcParams['mathtext.fallback_to_cm'] = True

    # The default font to use for math.
    # Can be any of the LaTeX font names, including
    # the special name "regular" for the same font
    # used in regular text.
    mpl.rcParams['mathtext.default'] = 'it'

    ### AXES
    # default face and edge color, default tick sizes,
    # default fontsizes for ticklabels, and so on.  See
    # http://matplotlib.org/api/axes_api.html#module-matplotlib.axes
    mpl.rcParams['axes.facecolor']      = 'white'       # axes background color
    mpl.rcParams['axes.edgecolor']      = 'black'       # axes edge color
    mpl.rcParams['axes.linewidth']      = 0.8           # edge linewidth
    mpl.rcParams['axes.grid']           = False         # display grid or not
    mpl.rcParams['axes.titlesize']      = 'large'       # fontsize of the axes title
    mpl.rcParams['axes.titlepad']       = 6.0           # pad between axes and title in points
    mpl.rcParams['axes.labelsize']      = 'medium'      # fontsize of the x any y labels
    mpl.rcParams['axes.labelpad']       = 4.0           # space between label and axis
    mpl.rcParams['axes.labelweight']    = 'normal'      # weight of the x and y labels
    mpl.rcParams['axes.labelcolor']     = 'black'
    mpl.rcParams['axes.axisbelow']      = 'line'        # draw axis gridlines and ticks below
                                                        # patches (True); above patches but below
                                                        # lines ('line'); or above all (False)

    mpl.rcParams['axes.formatter.limits'] = -7, 7       # use scientific notation if log10
                                                        # of the axis range is smaller than the
                                                        # first or larger than the second

    # When True, format tick labels
    # according to the user's locale.
    # For example, use ',' as a decimal
    # separator in the fr_FR locale.
    mpl.rcParams['axes.formatter.use_locale'] = False

    # When True, use mathtext for scientific notation.
    mpl.rcParams['axes.formatter.use_mathtext'] = False
    if mpl.__version__ >= '2.1':
        mpl.rcParams['axes.formatter.min_exponent'] = 0       # minimum exponent to format in scientific notation

    # If True, the tick label formatter
    # will default to labeling ticks relative
    # to an offset when the data range is
    # small compared to the minimum absolute
    # value of the data.
    mpl.rcParams['axes.formatter.useoffset'] = True

    # When useoffset is True, the offset
    # will be used when it can remove
    # at least this number of significant
    # digits from tick labels.
    mpl.rcParams['axes.formatter.offset_threshold'] = 4


    mpl.rcParams['axes.spines.left']   = True   # display axis spines
    mpl.rcParams['axes.spines.bottom'] = True
    mpl.rcParams['axes.spines.top']    = True
    mpl.rcParams['axes.spines.right']  = True


    # use unicode for the minus symbol
    # rather than hyphen.  See
    # http://en.wikipedia.org/wiki/Plus_and_minus_signs#Character_codes
    mpl.rcParams['axes.unicode_minus']  = True

    # How to scale axes limits to the data.
    # Use "data" to use data limits, plus some margin
    # Use "round_number" move to the nearest "round" number
    mpl.rcParams['axes.autolimit_mode'] = 'data'
    mpl.rcParams['axes.xmargin']        = .05  # x margin.  See `axes.Axes.margins`
    mpl.rcParams['axes.ymargin']        = .05  # y margin See `axes.Axes.margins`

    mpl.rcParams['polaraxes.grid']      = True    # display grid on polar axes
    mpl.rcParams['axes3d.grid']         = True    # display grid on 3d axes

    ### DATES
    mpl.rcParams['date.autoformatter.year']     = '%Y'
    mpl.rcParams['date.autoformatter.month']    = '%Y-%m'
    mpl.rcParams['date.autoformatter.day']      = '%Y-%m-%d'
    mpl.rcParams['date.autoformatter.hour']     = '%m-%d %H'
    mpl.rcParams['date.autoformatter.minute']   = '%d %H:%M'
    mpl.rcParams['date.autoformatter.second']   = '%H:%M:%S'
    mpl.rcParams['date.autoformatter.microsecond']   = '%M:%S.%f'

    ### TICKS
    # see http://matplotlib.org/api/axis_api.html#matplotlib.axis.Tick
    mpl.rcParams['xtick.top']            = False    # draw ticks on the top side
    mpl.rcParams['xtick.bottom']         = True     # draw ticks on the bottom side
    mpl.rcParams['xtick.major.size']     = 3.5      # major tick size in points
    mpl.rcParams['xtick.minor.size']     = 2        # minor tick size in points
    mpl.rcParams['xtick.major.width']    = 0.8      # major tick width in points
    mpl.rcParams['xtick.minor.width']    = 0.6      # minor tick width in points
    mpl.rcParams['xtick.major.pad']      = 3.5      # distance to major tick label in points
    mpl.rcParams['xtick.minor.pad']      = 3.4      # distance to the minor tick label in points
    mpl.rcParams['xtick.color']          = 'k'      # color of the tick labels
    mpl.rcParams['xtick.labelsize']      = 'medium' # fontsize of the tick labels
    mpl.rcParams['xtick.direction']      = 'out'    # direction: in, out, or inout
    mpl.rcParams['xtick.minor.visible']  = False    # visibility of minor ticks on x-axis
    mpl.rcParams['xtick.major.top']      = True     # draw x axis top major ticks
    mpl.rcParams['xtick.major.bottom']   = True     # draw x axis bottom major ticks
    mpl.rcParams['xtick.minor.top']      = True     # draw x axis top minor ticks
    mpl.rcParams['xtick.minor.bottom']   = True     # draw x axis bottom minor ticks

    mpl.rcParams['ytick.left']           = True     # draw ticks on the left side
    mpl.rcParams['ytick.right']          = False    # draw ticks on the right side
    mpl.rcParams['ytick.major.size']     = 3.5      # major tick size in points
    mpl.rcParams['ytick.minor.size']     = 2        # minor tick size in points
    mpl.rcParams['ytick.major.width']    = 0.8      # major tick width in points
    mpl.rcParams['ytick.minor.width']    = 0.6      # minor tick width in points
    mpl.rcParams['ytick.major.pad']      = 3.5      # distance to major tick label in points
    mpl.rcParams['ytick.minor.pad']      = 3.4      # distance to the minor tick label in points
    mpl.rcParams['ytick.color']          = 'k'      # color of the tick labels
    mpl.rcParams['ytick.labelsize']      = 'medium' # fontsize of the tick labels
    mpl.rcParams['ytick.direction']      = 'out'    # direction: in, out, or inout
    mpl.rcParams['ytick.minor.visible']  = False    # visibility of minor ticks on y-axis
    mpl.rcParams['ytick.major.left']     = True     # draw y axis left major ticks
    mpl.rcParams['ytick.major.right']    = True     # draw y axis right major ticks
    mpl.rcParams['ytick.minor.left']     = True     # draw y axis left minor ticks
    mpl.rcParams['ytick.minor.right']    = True     # draw y axis right minor ticks


    ### GRIDS
    mpl.rcParams['grid.color']          = 'b0b0b0'  # grid color
    mpl.rcParams['grid.linestyle']      = '-'       # solid
    mpl.rcParams['grid.linewidth']      = 0.8       # in points
    mpl.rcParams['grid.alpha']          = 1.0       # transparency, between 0.0 and 1.0

    ### Legend
    mpl.rcParams['legend.loc']           = 'best'
    mpl.rcParams['legend.frameon']       = True     # if True, draw the legend on a background patch
    mpl.rcParams['legend.framealpha']    = 0.8      # legend patch transparency
    mpl.rcParams['legend.facecolor']     = 'inherit'  # inherit from axes.facecolor; or color spec
    mpl.rcParams['legend.edgecolor']     = '0.8'      # background patch boundary color
    mpl.rcParams['legend.fancybox']      = True     # if True, use a rounded box for the
                                                    # legend background, else a rectangle
    mpl.rcParams['legend.shadow']        = False    # if True, give background a shadow effect
    mpl.rcParams['legend.numpoints']     = 1        # the number of marker points in the legend line
    mpl.rcParams['legend.scatterpoints'] = 1        # number of scatter points
    mpl.rcParams['legend.markerscale']   = 1.0      # the relative size of legend markers vs. original
    mpl.rcParams['legend.fontsize']      = 'medium'
    # Dimensions as fraction of fontsize:
    mpl.rcParams['legend.borderpad']     = 0.4      # border whitespace
    mpl.rcParams['legend.labelspacing']  = 0.5      # the vertical space between the legend entries
    mpl.rcParams['legend.handlelength']  = 2.0      # the length of the legend lines
    mpl.rcParams['legend.handleheight']  = 0.7      # the height of the legend handle
    mpl.rcParams['legend.handletextpad'] = 0.8      # the space between the legend line and legend text
    mpl.rcParams['legend.borderaxespad'] = 0.5      # the border between the axes and legend edge
    mpl.rcParams['legend.columnspacing'] = 2.0      # column separation

    ### FIGURE
    # See http://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure
    mpl.rcParams['figure.titlesize'] = 'large'      # size of the figure title (Figure.suptitle())
    mpl.rcParams['figure.titleweight'] = 'normal'   # weight of the figure title
    mpl.rcParams['figure.figsize']   = 6.4, 4.8     # figure size in inches
    mpl.rcParams['figure.dpi']       = 100          # figure dots per inch
    mpl.rcParams['figure.facecolor'] = 'white'      # figure facecolor; 0.75 is scalar gray
    mpl.rcParams['figure.edgecolor'] = 'white'      # figure edgecolor
    mpl.rcParams['figure.autolayout'] = False       # When True, automatically adjust subplot
                                                    # parameters to make the plot fit the figure
    mpl.rcParams['figure.max_open_warning'] = 20    # The maximum number of figures to open through
                                                    # the pyplot interface before emitting a warning.
                                                    # If less than one this feature is disabled.

    # The figure subplot parameters.  All dimensions are a fraction of the
    mpl.rcParams['figure.subplot.left']    = 0.125  # the left side of the subplots of the figure
    mpl.rcParams['figure.subplot.right']   = 0.9    # the right side of the subplots of the figure
    mpl.rcParams['figure.subplot.bottom']  = 0.11   # the bottom of the subplots of the figure
    mpl.rcParams['figure.subplot.top']     = 0.88   # the top of the subplots of the figure
    mpl.rcParams['figure.subplot.wspace']  = 0.2    # the amount of width reserved for blank space between subplots,
                                                    # expressed as a fraction of the average axis width
    mpl.rcParams['figure.subplot.hspace']  = 0.2    # the amount of height reserved for white space between subplots,
                                                    # expressed as a fraction of the average axis height


    ### IMAGES
    mpl.rcParams['image.aspect']            = 'equal'   # equal | auto | a number
    mpl.rcParams['image.interpolation']     = 'nearest' # see help(imshow) for options
    mpl.rcParams['image.cmap']              = 'viridis' # A colormap name, gray etc...
    mpl.rcParams['image.lut']               = 256       # the size of the colormap lookup table
    mpl.rcParams['image.origin']            = 'upper'   # lower | upper
    mpl.rcParams['image.resample']          = True
    mpl.rcParams['image.composite_image']   = True      # When True, all the images on a set of axes are
                                                        # combined into a single composite image before
                                                        # saving a figure as a vector graphics file,
                                                        # such as a PDF.

    ### CONTOUR PLOTS
    mpl.rcParams['contour.negative_linestyle'] = 'dashed'   # string or on-off ink sequence
    mpl.rcParams['contour.corner_mask']        = True       # True | False | legacy

    ### ERRORBAR PLOTS
    mpl.rcParams['errorbar.capsize'] = 0                    # length of end cap on error bars in pixels

    ### HISTOGRAM PLOTS
    mpl.rcParams['hist.bins'] = 10                  # The default number of histogram bins.
                                                    # If Numpy 1.11 or later is
                                                    # installed, may also be `auto`

    ### SCATTER PLOTS
    mpl.rcParams['scatter.marker'] = 'o'               # The default marker type for scatter plots.

    ### SAVING FIGURES
    mpl.rcParams['path.simplify'] = True            # When True, simplify paths by removing "invisible"
                                                    # points to reduce file size and increase rendering
                                                    # speed
    mpl.rcParams['path.simplify_threshold'] = 0.1   # The threshold of similarity below which
                                                    # vertices will be removed in the simplification
                                                    # process
    mpl.rcParams['path.snap'] = True                # When True, rectilinear axis-aligned paths will be snapped to
                                                    # the nearest pixel when certain criteria are met.  When False,
                                                    # paths will never be snapped.
    mpl.rcParams['path.sketch'] = None              # May be none, or a 3-tuple of the form (scale, length,
                                                    # randomness).
                                                    # *scale* is the amplitude of the wiggle
                                                    # perpendicular to the line (in pixels).  *length*
                                                    # is the length of the wiggle along the line (in
                                                    # pixels).  *randomness* is the factor by which
                                                    # the length is randomly scaled.

    # the default savefig params can be different from the display params
    # e.g., you may want a higher resolution, or to make the figure
    # background white
    mpl.rcParams['savefig.dpi']         = 'figure'      # figure dots per inch or 'figure'
    mpl.rcParams['savefig.facecolor']   = 'white'       # figure facecolor when saving
    mpl.rcParams['savefig.edgecolor']   = 'white'       # figure edgecolor when saving
    mpl.rcParams['savefig.format']      = 'pdf'         # png, ps, pdf, svg
    mpl.rcParams['savefig.bbox']        = 'standard'    # 'tight' or 'standard'.
                                                        # 'tight' is incompatible with pipe-based animation
                                                        # backends but will workd with temporary file based ones:
                                                        # e.g. setting animation.writer to ffmpeg will not work,
                                                        # use ffmpeg_file instead
    mpl.rcParams['savefig.pad_inches']      = 0.1       # Padding to be used when bbox is set to 'tight'
    mpl.rcParams['savefig.jpeg_quality']    = 95        # when a jpeg is saved, the default quality parameter.
    mpl.rcParams['savefig.directory']       = '~'       # default directory in savefig dialog box,
                                                        # leave empty to always use current working directory
    mpl.rcParams['savefig.transparent']     = False     # setting that controls whether figures are saved with a
                                                        # transparent background by default
