from .ProbePlotter import *
from .statistics import impl_plots
import numpy as np
import scipy as sc


class H5Plotter(ProbePlotter):

    def __init__(self):
        pass


    def plot_phase_space(self, xvar, yvar, **kwargs):
        """Plot a 2D phase space plot.

        Parameters
        ----------
        xvar : str
            Variable for x-axis
        yvar : str
            Variable for y-axis
        step : int, optional
            Step of dataset
        bins  : list or integer, optional
            Color energy bins
        xscale : str, optional
            'linear', 'log'
        yscale  : str, optional
            'linear', 'log'
        xsci : bool, optional
            x-ticks in scientific notation
        ysci : bool, optional
            y-ticks in scientific notation
        markersize: int
            Size of markers in scatter plot

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        try:
            step       = kwargs.pop('step', 0)
            bins       = kwargs.pop('bins', False)
            bunches    = kwargs.pop('bunches', [])
            markersize = kwargs.pop('markersize', 1)

            plt.xscale(kwargs.pop('yscale', 'linear'))
            plt.yscale(kwargs.pop('xscale', 'linear'))

            if kwargs.pop('xsci', False):
                plt.ticklabel_format(style='sci', axis='x', scilimits=(0,3))

            if kwargs.pop('ysci', False):
                plt.ticklabel_format(style='sci', axis='y', scilimits=(0,3))

            xdata = self.ds.getData(xvar, step=step)
            ydata = self.ds.getData(yvar, step=step)

            if bins:
                bdata = self.ds.getData('bin', step=step)
                bmax = np.max(bdata)
                nBins = bmax + 1

                for b in range(nBins):
                    xbin = xdata[bdata == b]
                    ybin = ydata[bdata == b]
                    plt.scatter(xbin, ybin, marker='.', s=markersize, **kwargs)
            elif bunches:
                bdata = self.ds.getData('bunchNumber', step=step)
                # get all bunches
                bmin = np.min(bdata)
                bmax = np.max(bdata)
                # 27. March 2018
                # https://stackoverflow.com/questions/6486450/python-compute-list-difference
                skipped = set(range(bmin, bmax+1)) - set(bunches)

                nBunches = bmax - bmin + 1
                colors = np.linspace(0, 1, nBunches + 1)

                # plot all skipped bunches with same color
                for i, s in enumerate(skipped):
                    xbin = xdata[bdata == s]
                    ybin = ydata[bdata == s]
                    lab = None
                    if i == 0:
                        lab = 'others'
                    plt.scatter(xbin, ybin, marker='.', s=markersize,
                                color=plt.cm.tab20(colors[nBunches]),
                                label=lab, **kwargs)
                for i, b in enumerate(bunches):
                    xbin = xdata[bdata == b]
                    ybin = ydata[bdata == b]
                    plt.scatter(xbin, ybin, marker='.',
                                s=markersize, color=plt.cm.tab20(colors[i]),
                                label='bunch ' + str(i), **kwargs)
                plt.legend(loc = 'upper center',
                        ncol=4, labelspacing=0.5,
                        bbox_to_anchor=(0.5, 1.1, 0.0, 0.0))
            else:
                plt.scatter(xdata, ydata, marker='.', s=markersize, **kwargs)

            xunit  = self.ds.getUnit(xvar)
            yunit  = self.ds.getUnit(yvar)
            xlabel = self.ds.getLabel(xvar)
            ylabel = self.ds.getLabel(yvar)

            plt.xlabel(xlabel + ' [' + xunit + ']')
            plt.ylabel(ylabel + ' [' + yunit + ']')

            plt.tight_layout()

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()


    def plot_density(self, xvar, yvar, **kwargs):
        """
        Do a density plot.

        Parameters
        ----------
        xvar : str
            x-axis variable to consider
        yvar : str
            y-axis variable to consider
        step : int, optional
            Step of dataset
        bins : array_like or int, optional
            Number of bins
        cmap : (matplotlib.pyplot.Colormap, str), optional
            Color map

        References
        ----------
        (22. March 2018)
        https://stackoverflow.com/questions/20105364/how-can-i-make-a-scatter-plot-colored-by-density-in-matplotlib

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        try:
            step = kwargs.pop('step', 0)
            bins = kwargs.pop('bins', (50,50))
            cmap = kwargs.pop('cmap', plt.cm.jet)

            xdata = self.ds.getData(xvar, step=step)
            ydata = self.ds.getData(yvar, step=step)

            xy = np.vstack([xdata, ydata])
            plt.hist2d(xdata, ydata, bins = bins, cmap=cmap)

            xunit  = self.ds.getUnit(xvar)
            yunit  = self.ds.getUnit(yvar)
            xlabel = self.ds.getLabel(xvar)
            ylabel = self.ds.getLabel(yvar)

            plt.xlabel(xlabel + ' [' + xunit + ']')
            plt.ylabel(ylabel + ' [' + yunit + ']')

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()


    def plot_histogram(self, var, **kwargs):
        """Plot a 1D histogram.

        Parameters
        ----------
        var : str
            Variable to consider
        step : int, optional
            Step of dataset
        bins : int or str, optional
            Binning type or number of bins
            (see https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.histogram.html)
        density : bool, optional
            Normalize such that integral over
                                range is 1.

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        try:
            step    = kwargs.pop('step', 0)
            bins    = kwargs.pop('bins', 'sturges')
            density = kwargs.pop('density', True)

            data = self.ds.getData(var, step=step)

            plt.hist(data, bins=bins, density=density)

            xunit  = self.ds.getUnit(var)
            xlabel = self.ds.getLabel(var)

            plt.xlabel(xlabel + ' [' + xunit + ']')

            ylabel = '#entries'

            if density:
                ylabel += ' (normalized)'
            plt.ylabel(ylabel)

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()


    def plot_classification(self, xvar, yvar, value, **kwargs):
        """Classification Plot

        Scatter plot where the points are colored according
        the value of the probability density function
        pdf(x, y) computed through kernel density estimation.

        Parameters
        ----------
        xvar : str
            x-axis variable to consider
        yvar : str
            y-axis variable to consider
        value : float
            Boundary value of classification
        step : int, optional
            Step of dataset

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        try:
            step    = kwargs.pop('step', 0)

            xdata = self.ds.getData(xvar, step=step)
            ydata = self.ds.getData(yvar, step=step)

            xunit  = self.ds.getUnit(xvar)
            xlabel = self.ds.getLabel(xvar)

            yunit  = self.ds.getUnit(yvar)
            ylabel = self.ds.getLabel(yvar)

            if xdata.size < 1 or ydata.size < 1:
                raise ValueError('Empty data container.')

            values = np.vstack([xdata, ydata])

            kde = sc.stats.gaussian_kde(values)
            pdf = kde.evaluate(values)

            lidx = np.where(pdf < value)
            gidx = np.where(pdf >= value)

            l = plt.scatter(xdata[lidx], ydata[lidx], c='r', s=20, edgecolor='', marker='.')
            g = plt.scatter(xdata[gidx], ydata[gidx], c='k', s=20, edgecolor='', marker='.')

            label = r'$pdf\left(' + xlabel + ', ' + xlabel + r'\right)$'
            plt.legend([l, g], [label + r'$ < $' + str(value), label + r'$ \geq $' + str(value)])

            plt.xlabel(xlabel + ' [' + xunit + ']')
            plt.ylabel(ylabel + ' [' + yunit + ']')

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()


    def plot_joint(self, xvar, yvar, join, **kwargs):
        """Do a joint plot (marginals + contour / scatter)

        Parameters
        ----------
        xvar : str
            x-axis variable to consider
        yvar : str
            y-axis variable to consider
        join : str
            'all', 'contour' or 'scatter'
        step : int, optional
            Step of dataset

        See Also
        --------
        visualization.statistics.impl_plots.plot_joint

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        try:
            step    = kwargs.pop('step', 0)

            xdata = self.ds.getData(xvar, step=step)
            ydata = self.ds.getData(yvar, step=step)

            xunit  = self.ds.getUnit(xvar)
            xlabel = self.ds.getLabel(xvar)

            yunit  = self.ds.getUnit(yvar)
            ylabel = self.ds.getLabel(yvar)

            plt = impl_plots.plot_joint(xdata, xlabel + ' [' + xunit + ']',
                                        ydata, ylabel + ' [' + yunit + ']',
                                        join, **kwargs)

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()


    def plot_density_scipy(self, xvar, yvar, **kwargs):
        """Do a density plot

        Parameters
        ----------
        xvar : str
            x-axis variable to consider
        yvar : str
            y-axis variable to consider
        step : int, optional
            Step of dataset
        nxbin : int, optional
            Number of bins for x-axis
        nybin : int, optional
            Number of bins for y-axis
        cmap : str, optional
            Colormap
        doShading : bool, optional
            If true, it uses 'gouraud' shading,
            else 'flat' shading
        xlim : tuple, optional
            If not specified use data to compute limits
        ylim : tuple, optional
            If not specified use data to compute limits
        clabel : str, optional
            Label of colorbar

        Notes
        -----
        https://matplotlib.org/examples/pylab_examples/pcolor_demo.html

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        try:
            step    = kwargs.pop('step', 0)

            xdata = self.ds.getData(xvar, step=step)
            ydata = self.ds.getData(yvar, step=step)

            xunit  = self.ds.getUnit(xvar)
            xlabel = self.ds.getLabel(xvar)

            yunit  = self.ds.getUnit(yvar)
            ylabel = "[" + self.ds.getLabel(yvar) + "]"


            if xdata.size < 1 or ydata.size < 1:
                raise ValueError('Empty data container.')


            nxbin     = kwargs.pop('nxbin', 300)
            nybin     = kwargs.pop('nybin', 300)
            cmap      = kwargs.pop('cmap', 'viridis')
            doShading = kwargs.pop('shading', False)
            xlim      = kwargs.pop('xlim', [])
            ylim      = kwargs.pop('ylim', [])
            clabel    = kwargs.pop('clabel', '')

            shading = 'flat'
            if doShading:
                shading = 'gouraud'

            # 19. March 2018
            # https://python-graph-gallery.com/85-density-plot-with-matplotlib/
            pdf = sc.stats.gaussian_kde([xdata, ydata])

            xmin = min(xdata)
            xmax = max(xdata)
            if xlim:
                xmin = xlim[0]
                xmax = xlim[1]

            ymin = min(ydata)
            ymax = max(ydata)
            if ylim:
                ymin = ylim[0]
                ymax = ylim[1]

            xi, yi = np.mgrid[xmin:xmax:nxbin*1j,
                              ymin:ymax:nybin*1j]
            zi = pdf(np.vstack([xi.flatten(), yi.flatten()]))

            pc = plt.pcolormesh(xi, yi, zi.reshape(xi.shape),
                                cmap=cmap, shading=shading)

            plt.axis([xmin, xmax, ymin, ymax])
            cb = plt.colorbar(pc)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            cb.set_label(clabel)

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()
