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

from .ProbePlotter import *
import numpy as np
import dask.array as da
import dask
import scipy as sc
import seaborn as sns

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
                bmax = (da.max(bdata)).compute()
                nBins = bmax + 1

                for b in range(nBins):
                    xbin = self._select(xdata, bdata, b, step)
                    ybin = self._select(ydata, bdata, b, step)
                    plt.scatter(xbin, ybin, marker='.', s=markersize, **kwargs)
            elif bunches:
                bdata = self.ds.getData('bunchNumber', step=step)
                # get all bunches
                bmin = (da.min(bdata)).compute()
                bmax = (da.max(bdata)).compute()
                # 27. March 2018
                # https://stackoverflow.com/questions/6486450/python-compute-list-difference
                skipped = set(range(bmin, bmax+1)) - set(bunches)

                nBunches = bmax - bmin + 1
                colors = np.linspace(0, 1, nBunches + 1)

                # plot all skipped bunches with same color
                for i, s in enumerate(skipped):
                    xbin = self._select(xdata, bdata, s, step)
                    ybin = self._select(ydata, bdata, s, step)
                    lab = None
                    if i == 0:
                        lab = 'others'
                    plt.scatter(xbin, ybin, marker='.', s=markersize,
                                color=plt.cm.tab20(colors[nBunches]),
                                label=lab, **kwargs)
                for i, b in enumerate(bunches):
                    xbin = self._select(xdata, bdata, b, step)
                    ybin = self._select(ydata, bdata, b, step)
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
            
            xy = da.vstack([xdata, ydata])
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

            values = da.vstack([xdata, ydata]).compute()

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
        marginals : str, optional
            'hist', 'kde', 'rug' or combination
            separated by '+', eg. 'hist+kde'
        size : int, optional
            Size of plot
        cmap : str, optional
            Colormap

        References
        ----------
        https://seaborn.pydata.org/generated/seaborn.JointGrid.html

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
            xlabel = "[" + self.ds.getLabel(xvar) + "]"
            
            yunit  = self.ds.getUnit(yvar)
            ylabel = "[" + self.ds.getLabel(yvar) + "]"

            if xdata.size < 1 or ydata.size < 1:
                raise ValueError('Empty data container.')

            marginals    = kwargs.pop('marginals', 'hist')
            size       = kwargs.pop('size', 8)
            cmap         = kwargs.pop('cmap', 'Blues_d')

            g = sns.JointGrid(x=xdata, y=ydata, size=size)

            hasJoin = False

            doAll = 'all' in join

            if 'scatter' in join or doAll:
                g = g.plot_joint(plt.scatter, marker='.', s=10, cmap=cmap)
                hasJoin = True

            if 'contour' in join or doAll:
                g = g.plot_joint(sns.kdeplot, shade=False, cmap=cmap)
                hasJoin = True

            g.set_axis_labels(xlabel, ylabel)

            if not hasJoin and not join == '':
                raise RuntimeError("Fill list either with 'scatter', " +
                                   "'contour', 'all'.")

            hist = 'hist' in marginals
            kde  = 'kde' in marginals
            rug  = 'rug' in marginals

            if hist:
                g = g.plot_marginals(sns.distplot, kde=kde, rug=rug)
            elif kde:
                g = g.plot_marginals(sns.kdeplot, shade=True)

            if rug and not hist:
                g = g.plot_marginals(sns.rugplot)

            hasMarginals = hist + kde + rug
            if not hasMarginals and not marginals == '':
                raise RuntimeError("Use either 'kde', 'hist', 'rug', " +
                                   "or combination with '+', e.g. hist+rug.")

            plt.tight_layout()
            
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
        Open issue: https://github.com/dask/dask/issues/2939

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        try:
            step    = kwargs.pop('step', 0)
            xdata = self.ds.getData(xvar, step=step).compute()
            ydata = self.ds.getData(yvar, step=step).compute()
            
            xunit  = self.ds.getUnit(xvar)
            xlabel = "[" + self.ds.getLabel(xvar) + "]"
            
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
            zi = pdf(da.vstack([xi.flatten(), yi.flatten()]))

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
