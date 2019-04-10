from .BasePlotter import *
import numpy as np

from .formatter import FormatScalarFormatter
import os

class SamplerPlotter(BasePlotter):
    
    def __init__(self):
        pass
    
    
    def plot_variability(self, fname, xvar, yvar, **kwargs):
        """
        Plot the mean, min and max over all samples.
        
        Parameters
        ----------
        fname   (str)           file containing the data (xvar and yvar) 
        xvar    (str)           x-axis data
        yvar    (str)           y-axis data
        
        Optional
        --------
        idx     (bool)          fix the x-axis labels (takes the original
                                data order but uses the indices to plot
                                and the values as ticks), useful for
                                periodic values (e.g. azimuth)
        nticks  (int)           number of ticks on axes (only for idx=True)
    
        Returns
        -------
        a matplotlib.pyplot handle
        """
        from opal import load_dataset
        
        nsamples = self.ds.size
    
        dirname = os.path.dirname(self.ds.filename)
        sdir = os.path.join(dirname, str(0))
        out = load_dataset(sdir, fname=fname, info=False)
        ydata = np.zeros(out.size, dtype=np.float)
        ymin  = np.finfo(np.float).max + np.zeros(out.size, dtype=np.float)
        ymax  = np.finfo(np.float).min + np.zeros(out.size, dtype=np.float)
    
        xdata = out.getData(xvar, **kwargs)
    
        nticks = kwargs.pop('nticks', 10)
    
        for i in range(nsamples):
            # load simulation directory
            sdir = os.path.join(dirname, str(i))
            out = load_dataset(sdir, fname=fname, info=False)
            data = out.getData(yvar, **kwargs)
            ydata += data
            ymin = np.minimum(ymin, data)
            ymax = np.maximum(ymax, data)
    
        mean = np.zeros(len(ydata), dtype=np.float)
        mean = ydata / np.float(nsamples)
    
        if not kwargs.pop('idx', False):
            plt.plot(xdata, mean, **kwargs, color='black', linestyle='dashed', label='mean')
            plt.fill_between(xdata, ymin, ymax,
                             facecolor='blue', alpha=0.2, label='variability region')
        else:
            l = len(xdata)
            ind = np.linspace(0, l-1, l, dtype=int)
            plt.plot(ind, mean, **kwargs, color='black', linestyle='dashed', label='mean')
            plt.fill_between(ind, ymin, ymax,
                             facecolor='blue', alpha=0.2, label='variability region')
            t = int(l / nticks) - 1
            plt.xticks(ind[::t], np.round(xdata, 0)[::t].astype(int))
    
        plt.legend(loc = 'upper center',
                   ncol=2, labelspacing=0.5,
                   bbox_to_anchor=(0.5, 1.1, 0.0, 0.0))
    
        plt.gca().ticklabel_format(axis='y', style='sci', scilimits=(-2, 2),
                                   useMathText=True, useOffset=True)
        
        xlabel = out.getLabel(xvar)
        xunit  = out.getUnit(xvar)
        
        ylabel = out.getLabel(yvar)
        yunit  = out.getUnit(yvar)

        plt.xlabel(xlabel + ' [' + xunit + ']')
        plt.ylabel(ylabel + ' [' + yunit + ']')
        plt.tight_layout()
    
        return plt


    def plot_sample_input_statistics(self, **kwargs):
        """
        Bar plot showing the number of samples per design variable.
        This makes only sense for sampling with only a few states.
        
        Parameters
        ----------
        None
        
        Optional
        --------
        None
    
        Returns
        -------
        a matplotlib.pyplot handle
        """
        # 10. April 2019
        # https://docs.python.org/2/library/collections.html
        from collections import Counter
        
        dvars = self.ds.design_variables
        
        nvar = len(dvars)
        
        counters = [Counter()] * nvar
        
        for i in range(self.ds.size):
            for j, dvar in enumerate(dvars):
                counters[j][self.ds.getData(var=dvar, ind=i)] += 1
        
        for j, dvar in enumerate(dvars):
            # 10. April 2019
            # https://stackoverflow.com/questions/12282232/how-do-i-count-unique-values-inside-a-list
            values = counters[j].values()
            curr = 0
            for val in values:
                plt.bar(np.arange(nvar), val, bottom=curr, width=1.0 / nvar)
                curr += val
        
        plt.xticks(np.arange(nvar), dvars)
        plt.ylabel('#occurrences')
        
        return plt
