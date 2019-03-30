from .ProbePlotter import *
from .statistics import impl_plots
import numpy as np

class H5Plotter(ProbePlotter):
    
    def __init__(self):
        pass
    
    
    def plot_phase_space(self, xvar, yvar, **kwargs):
        """
        Plot a 2D phase space plot.
        
        Parameters
        ----------
        xvar    (str)               variable for x-axis
        yvar    (str)               variable for y-axis
        
        Optional parameters
        -------------------
        step    (int)               of dataset
        bins    (list or integer)   color energy bins
        xscale  (str)               'linear', 'log'
        yscale  (str)               'linear', 'log'
        xsci    (bool)              x-ticks in scientific notation
        ysci    (bool)              y-ticks in scientific notation
    
        Returns
        -------
        a matplotlib.pyplot handle
        """
        step    = kwargs.pop('step', 0)
        bins    = kwargs.pop('bins', [])
        bunches = kwargs.pop('bunches', [])
        
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
            
            # get all bins not in plotted
            bmin = min(bdata)
            bmax = max(bdata)
            # 27. March 2018
            # https://stackoverflow.com/questions/6486450/python-compute-list-difference
            skipped = set(range(bmin, bmax+1)) - set(bins)
            
            nBins = bmax - bmin + 1
            colors = np.linspace(0, 1, nBins + 1)
            
            for i, b in enumerate(bins):
                xbin = xdata[np.where(bdata == b)]
                ybin = ydata[np.where(bdata == b)]
                plt.scatter(xbin, ybin, marker='.', s=1, color=plt.cm.tab20(colors[i]))
            # plot all skipped bins with same color
            for s in skipped:
                xbin = xdata[np.where(bdata == s)]
                ybin = ydata[np.where(bdata == s)]
                plt.scatter(xbin, ybin, marker='.', s=1, color=plt.cm.tab20(colors[nBins]))
        elif bunches:
            bdata = self.ds.getData('bunchNumber', step=step)
            # get all bunches
            bmin = min(bdata)
            bmax = max(bdata)
            # 27. March 2018
            # https://stackoverflow.com/questions/6486450/python-compute-list-difference
            skipped = set(range(bmin, bmax+1)) - set(bunches)
            
            nBunches = bmax - bmin + 1
            colors = np.linspace(0, 1, nBunches + 1)
            
            # plot all skipped bunches with same color
            for i, s in enumerate(skipped):
                xbin = xdata[np.where(bdata == s)]
                ybin = ydata[np.where(bdata == s)]
                lab = None
                if i == 0:
                    lab = 'others'
                plt.scatter(xbin, ybin, marker='.', s=1,
                            color=plt.cm.tab20(colors[nBunches]),
                            label=lab)
            for i, b in enumerate(bunches):
                xbin = xdata[np.where(bdata == b)]
                ybin = ydata[np.where(bdata == b)]
                plt.scatter(xbin, ybin, marker='.',
                            s=1, color=plt.cm.tab20(colors[i]),
                            label='bunch ' + str(i))
            plt.legend(loc = 'upper center',
                    ncol=4, labelspacing=0.5,
                    bbox_to_anchor=(0.5, 1.1, 0.0, 0.0))
        else:
            plt.scatter(xdata, ydata, marker='.', s=1)
    
        xunit  = self.ds.getUnit(xvar)
        yunit  = self.ds.getUnit(yvar)
        xlabel = self.ds.getLabel(xvar)
        ylabel = self.ds.getLabel(yvar)
        
        plt.xlabel(xlabel + ' [' + xunit + ']')
        plt.ylabel(ylabel + ' [' + yunit + ']')
        
        plt.tight_layout()
        
        return plt


    def plot_density(self, xvar, yvar, **kwargs):
        """
        Do a density plot.
        
        Parameters
        ----------
        xvar    (str)               x-axis variable to consider
        yvar    (str)               y-axis variable to consider
        
        Optional parameters
        -------------------
        step    (int)           of dataset
        bins    (list, array or integer) number of bins
        cmap    (Colormap, string)  color map
        
        Reference (22. March 2018)
        ---------
        https://stackoverflow.com/questions/20105364/how-can-i-make-a-scatter-plot-colored-by-density-in-matplotlib
        
        Returns
        -------
        a matplotlib.pyplot handle
        """
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


    def plot_histogram(self, var, **kwargs):
        """
        Plot a 1D histogram.
        
        Parameters
        ----------
        ds      (DatasetBase)       dataset
        var     (str)               variable to consider
        
        Optional parameters
        -------------------
        step    (int)           of dataset
        bins    (int /str)      binning type or #bins
                                (see https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.histogram.html)
        density (bool)          normalize such that integral over
                                range is 1.
        
        Returns
        -------
        a matplotlib.pyplot handle
        """
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


    def plot_classification(self, xvar, yvar, value, **kwargs):
        """
        Scatter plot where the points are colored according
        the value of the probability density function
        pdf(x, y) computed through kernel density estimation.
        
        Parameters
        ----------
        ds      (DatasetBase)       dataset
        xvar    (str)               x-axis variable to consider
        yvar    (str)               y-axis variable to consider
        value   (float)             boundary value of classification
        
        Optional parameters
        -------------------
        step    (int)           of dataset
        
        Returns
        -------
        a matplotlib.pyplot handle
        """
        step    = kwargs.pop('step', 0)
        
        xdata = self.ds.getData(xvar, step=step)
        ydata = self.ds.getData(yvar, step=step)
        
        xunit  = self.ds.getUnit(xvar)
        xlabel = self.ds.getLabel(xvar)
        
        yunit  = self.ds.getUnit(yvar)
        ylabel = self.ds.getLabel(yvar)
        
        plt = impl_plots.plot_classification(xdata, xlabel,
                                            ydata, ylabel,
                                            value)
        
        plt.xlabel(xlabel + ' [' + xunit + ']')
        plt.ylabel(ylabel + ' [' + yunit + ']')
        
        return plt


    def plot_joint(self, xvar, yvar, join, **kwargs):
        """
        Do a joint plot (marginals + contour / scatter)
        
        Parameters
        ----------
        ds      (DatasetBase)       dataset
        xvar    (str)               x-axis variable to consider
        yvar    (str)               y-axis variable to consider
        join    (str)               'all', 'contour' or 'scatter'
        
        Optional parameters
        -------------------
        step        (int)           of dataset
        see also                    help(impl_plots.plot_joint)
        
        Returns
        -------
        a matplotlib.pyplot handle
        """
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


    def plot_density_scipy(self, xvar, yvar, **kwargs):
        """
        Do a density plot
        
        Parameters
        ----------
        ds      (DatasetBase)       dataset
        xvar    (str)               x-axis variable to consider
        yvar    (str)               y-axis variable to consider
        
        Optional parameters
        -------------------
        step        (int)           of dataset
        see also                    help(impl_plots.plot_density)
        
        Returns
        -------
        a matplotlib.pyplot handle
        """
        step    = kwargs.pop('step', 0)
        
        xdata = self.ds.getData(xvar, step=step)
        ydata = self.ds.getData(yvar, step=step)
        
        xunit  = self.ds.getUnit(xvar)
        xlabel = self.ds.getLabel(xvar)
        
        yunit  = self.ds.getUnit(yvar)
        ylabel = self.ds.getLabel(yvar)
        clab   = ''
        
        plt = impl_plots.plot_density(xdata, xlabel + ' [' + xunit + ']',
                                    ydata, ylabel + ' [' + yunit + ']',
                                    clab, **kwargs)
        
        return plt
