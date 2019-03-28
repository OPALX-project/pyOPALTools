from opal.visualization.BasePlotter import *
from opal.parser.LatticeParser import LatticeParser
import os

class StatPlotter(BasePlotter):
    
    def __init__(self):
        pass


    def plot_profile1D(self, xvar, yvar, **kwargs):
        """
        Plot a 1D profile.
        
        Parameters
        ----------
        xvar    (str)           variable for x-axis
        yvar    (str)           variable for y-axis
        
        Optional parameters
        -------------------
        xscale  (str)               'linear', 'log'
        yscale  (str)               'linear', 'log'
        xsci    (bool)              x-ticks in scientific notation
        ysci    (bool)              y-ticks in scientific notation
        
        Returns
        -------
        a matplotlib.pyplot handle
        """
        plt.xscale(kwargs.pop('yscale', 'linear'))
        plt.yscale(kwargs.pop('xscale', 'linear'))
        
        if kwargs.pop('xsci', False):
            plt.ticklabel_format(style='sci', axis='x', scilimits=(0,3))
        
        if kwargs.pop('ysci', False):
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0,3))
        
        xdata = self.ds.getData(xvar)
        ydata = self.ds.getData(yvar)
        plt.plot(xdata, ydata, **kwargs)
        
        xunit  = self.ds.getUnit(xvar)
        yunit  = self.ds.getUnit(yvar)
        xlabel = self.ds.getLabel(xvar)
        ylabel = self.ds.getLabel(yvar)
        
        plt.xlabel(xlabel + ' [' + xunit + ']')
        plt.ylabel(ylabel + ' [' + yunit + ']')
        
        return plt

    
    def plot_envelope(dset, xvar='position', **kwargs):
        """
        Create an envelope plot.
        
        Author: Philippe Ganz
        Date:   2018
        
        Parameters
        ----------
        dset    (StatDataset)   another statistic dataset
        lfile   (str)           lattice file (*.lattice) (optional)
        xvar    (str)           x-axis variable
        
        Returns
        -------
        a matplotlib.pyplot handle
        """
        if not isinstance(dset, StatDataset):
            raise TypeError("Dataset '" + dset.filename +
                            "' is not an instance of 'StatDataset'.")
            
        lfile = kwargs.pop('lfile', '')
        
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, dpi=150)
        fig.set_size_inches(9,4)
        
        if lfile:
            lattice = LatticeParser()
            lattice.plot(lfile, fig, ax1, ax2)
        
        y1label = self.ds.getLabel('rms_x')
        y2label = self.ds.getLabel('rms_y')
        
        xunit = self.ds.getUnit(xvar)
        yunit = self.ds.getUnit('rms_x')
        
        dsets = [self.ds, dset]
    
        y1max = 0.0
        for ds in dsets:
            xdata  = ds.getData(xvar)
            y1data = ds.getData('rms_x')
            y1max  = max(max(y1data), y1max)
            ax1.plot(xdata, y1data, label=os.path.basename(ds.filename))
        
        # 27. March 2018
        # https://stackoverflow.com/questions/20350503/remove-first-and-last-ticks-label-of-each-y-axis-subplot
        plt.setp(ax1.get_yticklabels()[0], visible=False)
        
        ax2 = plt.gca()
    
        y2max = 0.0
        for ds in dsets:
            xdata =  ds.getData(xvar)
            y2data = ds.getData('rms_y')
            y2max  = max(max(y2data), y2max)
            ax2.plot(xdata, y2data)
        
        # 27. March 2018
        # https://stackoverflow.com/questions/925024/how-can-i-remove-the-top-and-right-axis-in-matplotlib
        ax1.spines['bottom'].set_visible(False)
        ax1.get_xaxis().set_visible(False)
        
        ax2.set_xlabel(xvar + ' [' + xunit + ']')
        
        ax1.set_ylabel(y1label + ' [' + yunit + ']')
        ax2.set_ylabel(y2label + ' [' + yunit + ']')
    
        ax1.set_ylim(bottom=0, top=y1max)
        ax2.set_ylim(bottom=0, top=y2max)
        # invert second y axis
        ax2.invert_yaxis()
        # show top spine on second axis (for matplotlib3)
        ax2.spines['top'].set_visible(True)
        
        ax1.legend(bbox_to_anchor=(0.6, 1.08))
        
        ax2.xaxis.set_label_position('bottom') 
        ax2.xaxis.set_ticks_position('bottom')
        
        fig.subplots_adjust(hspace = 0.0)
        return plt
