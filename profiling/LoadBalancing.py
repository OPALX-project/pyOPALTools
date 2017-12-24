##
# @author Matthias Frey
# @date 24. Dec. 2017
#

from utilities import SDDSParser
import matplotlib.pyplot as plt
import numpy as np
import warnings

class LoadBalancing:
    """
    Read in an OPAL *.mem file that is written using
    the option MEMORY=TRUE in the OPAL input file.
    """
    
    def __init__(self):
        self._sdds = []
        self._fname = ''
    
    
    def __read(self, fname):
        
        if fname == self._fname:
            return
        
        self._sdds = SDDSParser()
        self._sdds.parse(fname)
    
    def histogram(self, fname, **kwargs):
        
        self.__read(fname)
        
        saveas   = kwargs.get('saveas', None)
        figsize  = kwargs.get('figsize', (12, 12))
        grid     = kwargs.get('grid', False)
        title    = kwargs.get('title', None)
        yscale   = kwargs.get('yscale', 'linear')
        xscale   = kwargs.get('xscale', 'linear')
        fontsize = kwargs.get('fontsize', 10)
        blower   = kwargs.get('blower', [0.0, 0.0,  0.25, 0.5,  0.75])
        bupper   = kwargs.get('bupper', [0.0, 0.25, 0.5,  0.75, 1.0])
        
        if not len(blower) == len(bupper):
            raise RuntimeError('len(blower) != len(bupper)')
        
        nTotal = len(self._sdds.getVariables())
        nCols = sum('processor' in var for var in self._sdds.getVariables())
        
        
        time_unit = self._sdds.getUnitOfVariable('t')
        time = self._sdds.getDataOfVariable('t')
        
        nRows = len(time)
        
        # iterate through all steps and do a boxplot
        colStart = nTotal - nCols
        colEnd   = nCols + 1
        
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
        
        # percentages with respect to expected averaga number p / t
        # where p is the number of particles per processes and t the total
        # number of particles
        stamps = np.empty([nRows, len(blower)], dtype=float)
        
        p = 1.0 / nCols
        
        # each row is a time stamp
        for r in range(0, nRows):
            stamp = np.empty([nCols,], dtype=float)
            for c in range(colStart, colEnd+1):
                cc = c - colStart
                stamp[cc] = float(self._sdds.getDataOfVariable('processor-' + str(cc))[r])
            # total number of particles
            total = sum(stamp)
            
            # percentage []
            stamp /= total
            
            # check bin
            for i in range(0, len(blower)):
                
                if blower[i] == bupper[i]:
                    stamps[r, i] = ((blower[i] <= stamp) & (stamp <= bupper[i])).sum()
                else:
                    stamps[r, i] = ((blower[i] < stamp) & (stamp <= bupper[i])).sum()
        
        
        for i in range(0, len(blower)):
            
            common = str(blower[i]) + ', ' + str(bupper[i]) + ']'
            lab = ']' + common
            
            if blower[i] == bupper[i]:
                lab = '[' + common
            
            plt.plot(stamps[:, i], label=lab)
        
        plt.xlabel('time [' + time_unit + ']', fontsize=fontsize)
        plt.xticks(fontsize=fontsize)
        plt.xscale(xscale)
        
        plt.ylabel('#cores', fontsize=fontsize)
        plt.yticks(fontsize=fontsize)
        plt.yscale(yscale)
        
        plt.legend(fontsize=fontsize)
        
        plt.grid(grid)
        
        if title:
            plt.title(title, fontsize=fontsize)
        
        plt.tight_layout()
        if saveas:
            plt.savefig(saveas)
        else:
            plt.show()
    
    
    def summary(self, fname, **kwargs):
        
        self.__read(fname)
        
        saveas   = kwargs.get('saveas', None)
        figsize  = kwargs.get('figsize', (12, 12))
        grid     = kwargs.get('grid', False)
        title    = kwargs.get('title', None)
        yscale   = kwargs.get('yscale', 'linear')
        xscale   = kwargs.get('xscale', 'linear')
        fontsize = kwargs.get('fontsize', 10)
        
        nTotal = len(self._sdds.getVariables())
        nCols = sum('processor' in var for var in self._sdds.getVariables())
        
        
        time_unit = self._sdds.getUnitOfVariable('t')
        time = self._sdds.getDataOfVariable('t')
        
        nRows = len(time)
        
        # iterate through all steps and do a boxplot
        colStart = nTotal - nCols
        colEnd   = nCols + 1
        
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
        
        # each row is a time stamp
        minimum = []
        maximum = []
        mean    = []
        for r in range(0, nRows):
            stamp = np.empty([nCols,], dtype=float)
            for c in range(colStart, colEnd+1):
                cc = c - colStart
                stamp[cc] = float(self._sdds.getDataOfVariable('processor-' + str(cc))[r])
            minimum.append(min(stamp))
            mean.append(np.mean(stamp))
            maximum.append(max(stamp))
        
        plt.plot(time, minimum, label='minimum')
        plt.plot(time, maximum, label='maximum')
        plt.plot(time, mean, label='mean')
        
        plt.xlabel('time [' + time_unit + ']', fontsize=fontsize)
        plt.xticks(fontsize=fontsize)
        plt.xscale(xscale)
        
        plt.ylabel('#particles [ ]', fontsize=fontsize)
        plt.yticks(fontsize=fontsize)
        plt.yscale(yscale)
        
        plt.legend(fontsize=fontsize)
        
        plt.grid(grid)
        
        if title:
            plt.title(title, fontsize=fontsize)
        
        plt.tight_layout()
        if saveas:
            plt.savefig(saveas)
        else:
            plt.show()
    
    
    def boxplot(self, fname, **kwargs):
        
        self.__read(fname)
        
        saveas   = kwargs.get('saveas', None)
        figsize  = kwargs.get('figsize', (12, 12))
        grid     = kwargs.get('grid', False)
        title    = kwargs.get('title', None)
        yscale   = kwargs.get('yscale', 'linear')
        xscale   = kwargs.get('xscale', 'linear')
        fontsize = kwargs.get('fontsize', 10)
        
        nTotal = len(self._sdds.getVariables())
        nCols = sum('processor' in var for var in self._sdds.getVariables())
        
        
        time_unit = self._sdds.getUnitOfVariable('t')
        time = self._sdds.getDataOfVariable('t')
        
        nRows = len(time)
        
        # iterate through all steps and do a boxplot
        colStart = nTotal - nCols
        colEnd   = nCols + 1
        
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
        
        # each row is a time stamp
        stamps = []
        for r in range(0, nRows):
            stamp = np.empty([nCols,], dtype=float)
            for c in range(colStart, colEnd+1):
                cc = c - colStart
                stamp[cc] = float(self._sdds.getDataOfVariable('processor-' + str(cc))[r])
            stamps.append(stamp)
        
        if xscale == 'log':
            # 24. Dec. 2017
            # https://stackoverflow.com/questions/19328537/check-array-for-values-equal-or-very-close-to-zero
            # https://stackoverflow.com/questions/19141432/python-numpy-machine-epsilon
            if np.any(np.absolute(time) < np.finfo(float).eps):
                warnings.warn('Entry close to zero. Switching to linear x scale',
                              RuntimeWarning)
                xscale='linear'
        
        plt.boxplot(stamps, 0, '', positions=time)
        
        plt.xlabel('time [' + time_unit + ']', fontsize=fontsize)
        plt.xticks(fontsize=fontsize)
        plt.xscale(xscale)
        
        plt.ylabel('#particles [ ]', fontsize=fontsize)
        plt.yticks(fontsize=fontsize)
        plt.yscale(yscale)
        
        plt.grid(grid)
        
        if title:
            plt.title(title, fontsize=fontsize)
        
        plt.tight_layout()
        if saveas:
            plt.savefig(saveas)
        else:
            plt.show()
