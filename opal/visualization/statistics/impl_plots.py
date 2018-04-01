import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def plot_classifiction(xdata, xlab,
                       ydata, ylab,
                       prob):
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
    prob    (float)             probability [0, 1] to
                                classify
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    values = np.vstack([xdata, ydata])
    
    kde = stats.gaussian_kde(values)
    pdf = kde.evaluate(values)
    
    lidx = np.where(pdf < prob)
    gidx = np.where(pdf >= prob)
    l = plt.scatter(xdata[lidx], ydata[lidx], c='r', s=20, edgecolor='', marker='.')
    g = plt.scatter(xdata[gidx], ydata[gidx], c='k', s=20, edgecolor='', marker='.')
    
    label = r'$pdf\left(' + xlab + ', ' + ylab + r'\right)$'
    plt.legend([l, g], [label + r'$ < $' + str(prob), label + r'$ \geq $' + str(prob)])
    
    return plt
