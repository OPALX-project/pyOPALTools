from .BasePlotter import *
import numpy as np


class ProbePlotter(BasePlotter):
    
    def __init__(self):
        pass
    
    
    def plot_probe_histogram(self, **kwargs):
        """
        Plot a histogram of the probe histogram
        bin count vs. radius.
        
        Parameters
        ----------
        
        Optionals
        ---------
        grid    (bool)          draw grid
        scale   (bool)          scales to 1.0
                                (default: False)
        kwargs                  in case of H5: all arguments
                                of matplotlib.pyplot.hist
        
        Returns
        -------
        a matplotlib.pyplot handle
        """
        try:
            from opal import filetype
            
            ylabel = self.ds.getLabel('bincount')
            
            if self.ds.filetype == filetype.HIST:
                bincount = self.ds.getData('bincount')
                rmin = self.ds.getData('min')
                rmax = self.ds.getData('max')
                nbins = self.ds.getData('nbins')
                #dr = self.ds.getData('binsize')

                radius = np.linspace(float(rmin), float(rmax), nbins)

                if kwargs.pop('scale', False):
                    bincount = np.asarray(bincount) / max(bincount )
                    ylabel += ' (normalized)'

                plt.grid(kwargs.pop('grid', False))

                plt.plot(radius, bincount, **kwargs)
                plt.xlabel('radius [' + self.ds.getUnit('min') + ']')
            elif self.ds.filetype == filetype.H5:
                x = np.array([])
                y = np.array([])
                for s in range(self.ds.size):
                    x = np.append(x, self.ds.getData('x', step=s))
                    y = np.append(y, self.ds.getData('y', step=s))

                plt.hist(np.sqrt(x**2 + y**2), **kwargs)
                plt.xlabel('radius [' + self.ds.getUnit('x') + ']')

                if kwargs.pop('density', False):
                    ylabel = 'density'

            plt.ylabel(ylabel)

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()
