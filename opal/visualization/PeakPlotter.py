from .BasePlotter import *
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
        begin   (int)           first peak
        end     (int)           last peak
        
        Returns
        -------
        a matplotlib.pyplot handle
        """
        if isinstance(dset, list):
            raise ValueError('Exactly 1 datasets expected. ' +
                            'len(dsets) = ' + str(len(dset)) + ' != 1.')
        
        dsets = [self.ds, dset]
        
        for ds in dsets:
            from opal import filetype
            if not ds.filetype == filetype.PEAK:
                raise TypeError(ds.filename +
                                ' is not a peak (*.peaks) file.')
        
        unit = dsets[0].getUnit('radius')
        
        if not unit == dsets[1].getUnit('radius'):
            raise ValueError('Not same radius units.')
        
        peaks1 = dsets[0].getData('radius')
        peaks2 = dsets[1].getData('radius')
        
        npeaks = min(len(peaks1), len(peaks2))
        begin = kwargs.pop('begin', 0)
        end   = kwargs.pop('end', npeaks)
        
        if begin < 0:
            from opal.utilities.logger import opal_logger
            opal_logger.error("Invalid parameter value 'begin = " + str(begin) + "'")
        
        if end < begin or end > npeaks:
            from opal.utilities.logger import opal_logger
            opal_logger.error("Invalid parameter value 'end = " + str(end) + "'")
        
        p1 = peaks1[begin:end]
        p2 = peaks2[begin:end]
        
        npeaks = len(p2)
        
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
        
            xticks = range(begin, end)
            
            plt.plot(xticks, diff, 'o', **kwargs)
            
            plt.xlabel('peak number')
            
            plt.ylabel('peak difference [' + unit + ']')
        
        return plt
