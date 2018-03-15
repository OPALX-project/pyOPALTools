import seaborn as sns
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import warnings


def simple_kde_plot(xdata, ydata, **kwargs):
    xlab         = kwargs.get('xlab', 'x-axis')
    ylab         = kwargs.get('ylab', 'y-axis')
    size         = kwargs.get('size', 7)
    cmap         = kwargs.get('cmap', 'viridis')
    cbar         = kwargs.get('cbar', False)
    kernel       = kwargs.get('kernel', 'gau')
    bw           = kwargs.get('bw', 'scott')
    n_levels     = kwargs.get('n_levels', 6)
    shade        = kwargs.get('shade', False)
    shade_lowest = kwargs.get('shade_lowest', False)
    scipy        = kwargs.get('scipy', False)
    
    if scipy:
        if cbar:
            warnings.warn('SciPy mode: Colorbar not used.')
        
        if not kernel == 'gau':
            warnings.warn('SciPy mode: Only Gaussian Kernel supported.')
        
        xmin = xdata.min()
        xmax = xdata.max()
        ymin = ydata.min()
        ymax = ydata.max()
        
        X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
        positions = np.vstack([X.ravel(), Y.ravel()])
        values = np.vstack([xdata, ydata])
        kernel = stats.gaussian_kde(values)
        Z = np.reshape(kernel(positions).T, X.shape)
        
        cs = plt.contour(X, Y, Z, cmap=cmap)
        plt.clabel(cs, inline=True, fontsize=10)
        plt.xlabel(xlab)
        plt.ylabel(ylab)
    else:
        ax = sns.kdeplot(xdata, ydata,
                         kernel=kernel,
                         bw=bw,
                         cbar=cbar,
                         shade=shade,
                         shade_lowest=shade_lowest,
                         n_levels=n_levels,
                         cmap=cmap)
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)
