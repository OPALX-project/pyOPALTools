# Copyright (c) 2018 - 2019, Matthias Frey, Paul Scherrer Institut, Villigen PSI, Switzerland
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

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import seaborn as sns

def plot_classification(xdata, xlab,
                        ydata, ylab,
                        value):
    """Scatter plot where the points are colored according
    the value of the probability density function
    pdf(x, y) computed through kernel density estimation.

    Parameters
    ----------
    xdata : array_like
        Data of x-axis
    xlab : str
        Label of x-axis data
    ydata : array_like
        Data oy y-axis
    ylab : str
        Label of y-axis data
    value : float
        Boundary value of classification

    Returns
    -------
    matplotlib.pyplot
        Plot handle
    """
    if xdata.size < 1 or ydata.size < 1:
        raise ValueError('Empty data container.')

    values = np.vstack([xdata, ydata])

    kde = stats.gaussian_kde(values)
    pdf = kde.evaluate(values)

    lidx = np.where(pdf < value)
    gidx = np.where(pdf >= value)

    l = plt.scatter(xdata[lidx], ydata[lidx], c='r', s=20, edgecolor='', marker='.')
    g = plt.scatter(xdata[gidx], ydata[gidx], c='k', s=20, edgecolor='', marker='.')

    label = r'$pdf\left(' + xlab + ', ' + ylab + r'\right)$'
    plt.legend([l, g], [label + r'$ < $' + str(value), label + r'$ \geq $' + str(value)])

    return plt


def plot_joint(xdata, xlab,
               ydata, ylab,
               join, **kwargs):
    """Do a joint plot (marginals + contour / scatter).

    Parameters
    ----------
    xdata : array_like
        Data of x-axis
    xlab : str
        Label of x-axis data
    ydata : array_like
        Data oy y-axis
    ylab : str
        Label of y-axis data
    join : str
        'all', 'contour' or 'scatter'
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
    if xdata.size < 1 or ydata.size < 1:
        raise ValueError('Empty data container.')

    marginals    = kwargs.pop('marginals', 'hist')
    size         = kwargs.pop('size', 8)
    cmap         = kwargs.pop('cmap', 'Blues_d')

    g = sns.JointGrid(x=xdata, y=ydata, height=size)

    hasJoin = False

    doAll = 'all' in join

    if 'scatter' in join or doAll:
        g = g.plot_joint(plt.scatter, marker='.', s=10, cmap=cmap)
        hasJoin = True

    if 'contour' in join or doAll:
        g = g.plot_joint(sns.kdeplot, shade=False, cmap=cmap)
        hasJoin = True

    g.set_axis_labels(xlab, ylab)

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



def plot_density(xdata, xlab,
                 ydata, ylab,
                 clab, **kwargs):
    """Do a joint plot (marginals + contour / scatter).

    Parameters
    ----------
    xdata : array_like
        Data of x-axis
    xlab : str
        Label of x-axis data
    ydata : array_like
        Data oy y-axis
    ylab : str
        Label of y-axis data
    clab : str
        Label of colorbar
    nxbin : int, optional
        Number of bins for x-axis
    nybin : int, optional
        Number of bins for y-axis
    cmap : str, optional
        Colormap
    shading : bool, optional
        If true, it uses 'gouraud' shading,
        else 'flat' shading
    xlim : tuple, optional
        If not specified use data to compute limits
    ylim : tuple, optional
        If not specified use data to compute limits

    References
    ----------
    https://matplotlib.org/examples/pylab_examples/pcolor_demo.html

    Returns
    -------
    matplotlib.pyplot
        Plot handle
    """
    if xdata.size < 1 or ydata.size < 1:
        raise ValueError('Empty data container.')


    nxbin     = kwargs.pop('nxbin', 300)
    nybin     = kwargs.pop('nybin', 300)
    cmap      = kwargs.pop('cmap', 'viridis')
    doShading = kwargs.pop('shading', False)
    xlim      = kwargs.pop('xlim', [])
    ylim      = kwargs.pop('ylim', [])

    shading = 'flat'
    if doShading:
        shading = 'gouraud'

    # 19. March 2018
    # https://python-graph-gallery.com/85-density-plot-with-matplotlib/
    pdf = stats.gaussian_kde([xdata, ydata])

    xmin = xdata.min()
    xmax = xdata.max()
    if xlim:
        xmin = xlim[0]
        xmax = xlim[1]

    ymin = ydata.min()
    ymax = ydata.max()
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
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    cb.set_label(clab)

    return plt
