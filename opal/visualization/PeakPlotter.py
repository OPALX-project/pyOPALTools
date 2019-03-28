from opal.visualization.BasePlotter import *
import numpy as np
import os

class PeakPlotter(BasePlotter):
    
    def __init__(self):
        pass
    
    
    def plot_peak_difference(self, dset, **kwargs):
        """
        Plot the peak difference of a probe output.
        
        Parameters
        ----------
        dset   (PeakDataset)   a datasets
        
        Optionals
        ---------
        grid    (bool)          draw grid
        raxis   (bool)          do radius vs radius plot instead
        
        Returns
        -------
        a matplotlib.pyplot handle
        """
        if isinstance(dset, list):
            raise ValueError('Exactly 1 datasets expected. ' +
                            'len(dsets) = ' + str(len(dset)) + ' != 1.')
        
        dsets = [self.ds, dset]
        
        for ds in dsets:
            from opal.datasets.filetype import FileType
            if not ds.filetype == FileType.PEAK:
                raise TypeError(ds.filename +
                                ' is not a peak (*.peaks) file.')
        
        unit = dsets[0].getUnit('radius')
        
        if not unit == dsets[1].getUnit('radius'):
            raise ValueError('Not same radius units.')
        
        peaks1 = dsets[0].getData('radius')
        peaks2 = dsets[1].getData('radius')
        
        npeaks = min(len(peaks1), len(peaks2))
        p1 = peaks1[0:npeaks]
        p2 = peaks2[0:npeaks]
        
        plt.grid(kwargs.pop('grid', False))
        radiusPlot = kwargs.pop('raxis', False)
        
        if radiusPlot:
            lowest  = min(min(p1), min(p2))
            highest = max(max(p1), max(p2))
            
            plt.plot([lowest, highest], [lowest, highest],
                    linestyle='dashed', color='black',
                    label='y = x')
            
            plt.plot(p1, p2, marker='o', **kwargs)
            
            plt.xlabel('radius [' + unit + '] (' +
                    os.path.basename(dsets[0].filename) + ')')
            plt.ylabel('radius [' + unit + '] (' +
                    os.path.basename(dsets[1].filename) + ')')
        else:
            diff = p1 - p2
        
            xticks = range(1, npeaks + 1)
            
            #ylim = [min(diff) - 0.001, max(diff) + 0.001]
        
            plt.plot(xticks, diff, 'o', **kwargs)
            plt.xticks(xticks)
            #plt.ylim(ylim)
            
            plt.xlabel('peak number')
            
            plt.ylabel('peak difference [' + unit + ']')
        
        return plt
