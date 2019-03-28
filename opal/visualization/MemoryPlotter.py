# Author: Matthias Frey
# Date:   March 2018 - 2019

from opal.visualization.BasePlotter import *
import numpy as np
from opal.utilities.logger import opal_logger

class MemoryPlotter(BasePlotter):
    
    def __init__(self):
        pass
    
        def plot_total_memory(self, **kwargs):
        """
        Plot the total memory consumption vs. simulation time.
        
        """
        grid     = kwargs.pop('grid', False)
        title    = kwargs.pop('title', None)
        yscale   = kwargs.pop('yscale', 'linear')
        xscale   = kwargs.pop('xscale', 'linear')
        
        memory_usage = self.ds.getData('memory')
        time = self.ds.getData('t')
        plt.plot(time, memory_usage)
        
        plt.grid(grid, which='both')
        
        memory_unit = self.ds.getUnit('memory')
        time_unit = self.ds.getUnit('t')
        
        plt.xlabel('time [' + time_unit + ']')
        plt.xscale(xscale)
        
        plt.ylabel('total memory [' + memory_unit + ']')
        plt.yscale(yscale)
        
        if title:
            plt.title(title)
        
        plt.tight_layout()
        
        return plt


    def plot_memory_summary(self, **kwargs):
        """
        Plot the maximum, minimum and average memory consumption
        vs. simulation time.
        """
        grid     = kwargs.pop('grid', False)
        title    = kwargs.pop('title', None)
        yscale   = kwargs.pop('yscale', 'linear')
        xscale   = kwargs.pop('xscale', 'linear')
            
        nTotal = len(self.ds.getVariables())
        nCols = sum('processor' in var for var in self.ds.getVariables())
            
        
        time_unit = self.ds.getUnit('t')
        time = self.ds.getData('t')
        
        memory_unit = self.ds.getUnit('memory')
        
        nRows = len(time)
        
        # iterate through all steps and do a boxplot
        colStart = nTotal - nCols
        colEnd   = nCols + 1
        
        # each row is a time stamp
        minimum = []
        maximum = []
        mean    = []
        for r in range(0, nRows):
            stamp = np.empty([nCols,], dtype=float)
            for c in range(colStart, colEnd+1):
                cc = c - colStart
                stamp[cc] = float(self.ds.getData('processor-' + str(cc))[r])
            minimum.append(min(stamp))
            mean.append(np.mean(stamp))
            maximum.append(max(stamp))
        
        plt.plot(time, minimum, label='minimum')
        plt.plot(time, maximum, label='maximum')
        plt.plot(time, mean, label='mean')
        
        plt.xlabel('time [' + time_unit + ']')
        plt.xscale(xscale)
            
        plt.ylabel('memory [' + memory_unit + ']')
        plt.yscale(yscale)
        
        plt.legend()
        
        plt.grid(grid, which='both')
        
        if title:
            plt.title(title)
        
        plt.tight_layout()
        
        return plt


    def plot_memory_boxplot(self, **kwargs):
        grid     = kwargs.pop('grid', False)
        title    = kwargs.pop('title', None)
        yscale   = kwargs.pop('yscale', 'linear')
        xscale   = kwargs.pop('xscale', 'linear')
        
        nTotal = len(self.ds.getVariables())
        nCols = sum('processor' in var for var in self.ds.getVariables())
        
        time_unit = self.ds.getUnit('t')
        time = self.ds.getData('t')
        
        memory_unit = self.ds.getUnit('memory')
        
        nRows = len(time)
        
        # iterate through all steps and do a boxplot
        colStart = nTotal - nCols
        colEnd   = nCols + 1
        
        # each row is a time stamp
        stamps = []
        for r in range(0, nRows):
            stamp = np.empty([nCols,], dtype=float)
            for c in range(colStart, colEnd+1):
                cc = c - colStart
                stamp[cc] = float(self.ds.getData('processor-' + str(cc))[r])
            stamps.append(stamp)
        
        if xscale == 'log':
            # 24. Dec. 2017
            # https://stackoverflow.com/questions/19328537/check-array-for-values-equal-or-very-close-to-zero
            # https://stackoverflow.com/questions/19141432/python-numpy-machine-epsilon
            if np.any(np.absolute(time) < np.finfo(float).eps):
                opal_logger.warning('Entry close to zero. Switching to linear x scale')
                xscale='linear'
        
        plt.boxplot(stamps, 0, '', positions=time)
        
        plt.xlabel('time [' + time_unit + ']')
        plt.xscale(xscale)
        
        plt.ylabel('memory [' + memory_unit + ']')
        plt.yscale(yscale)
        
        plt.grid(grid, which='both')
        
        if title:
            plt.title(title)
        
        plt.tight_layout()
        
        return plt
