import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import seaborn as sns

def plot_classification(xdata, xlab,
                        ydata, ylab,
                        value):
    """
    Scatter plot where the points are colored according
    the value of the probability density function
    pdf(x, y) computed through kernel density estimation.
    
    Parameters
    ----------
    xdata   (array)             data of x-axis
    xlab    (str)               label of x-axis data
    ydata   (array)             data oy y-axis
    xlab    (str)               label of y-axis data
    value   (float)             boundary value of classification
    
    Returns
    -------
    a matplotlib.pyplot handle
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
    """
    
    Parameters
    ----------
    xdata   (array)     data of x-axis
    xlab    (str)       label of x-axis data
    ydata   (array)     data oy y-axis
    xlab    (str)       label of y-axis data
    join    (str)       'all', 'contour' or 'scatter'
    
    Optionals
    ---------
    marginals   (str)   'hist', 'kde', 'rug' or combination
                        separated by '+', eg. 'hist+kde'
    size        (int)   size of plot        
    cmap        (str)   colormap
    
    Reference
    ---------
    https://seaborn.pydata.org/generated/seaborn.JointGrid.html
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    if xdata.size < 1 or ydata.size < 1:
        raise ValueError('Empty data container.')
    
    marginals    = kwargs.get('marginals', 'hist')
    size         = kwargs.get('size', 8)
    cmap         = kwargs.get('cmap', 'Blues_d')
    
    g = sns.JointGrid(x=xdata, y=ydata, size=size)
    
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
