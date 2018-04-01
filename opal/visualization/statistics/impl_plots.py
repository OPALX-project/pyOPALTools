import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

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
