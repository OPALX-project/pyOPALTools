import seaborn as sns
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import warnings


def simple_kde_plot(xdata, ydata, **kwargs):
    xlab         = kwargs.get('xlab', 'x')
    ylab         = kwargs.get('ylab', 'y')
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
    
    
    return plt


def density_plot(xdata, ydata, **kwargs):
    """
    
    https://matplotlib.org/examples/pylab_examples/pcolor_demo.html
    """
    
    
    xlab      = kwargs.get('xlab', 'x')
    ylab      = kwargs.get('ylab', 'y')
    clab      = kwargs.get('clab', '')
    nxbin     = kwargs.get('nxbin', 300)
    nybin     = kwargs.get('nybin', 300)
    cmap      = kwargs.get('cmap', 'viridis')
    doShading = kwargs.get('shading', False)
    xlim      = kwargs.get('xlim', [])
    ylim      = kwargs.get('ylim', [])
    
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
    plt.xlabel(r'$' + xlab + '$')
    plt.ylabel(r'$' + ylab + '$')
    cb.set_label(r'$' + clab + '$')
    
    return plt
