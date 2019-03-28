from opal.visualization.TimingPlotter import *
import numpy as np

class StdOpalOutputPlotter(TimingPlotter):
    
    def __init__(self):
        pass
    
    
    def plot_RF_phases(self, RFcavity, **kwargs):
        """
        
        Parameters
        ----------
        RFcavity    ([str])         name of the RFcavity as specifed in the input file
        
        Returns
        -------
        a matplotlib.pyplot handle
        """
        data = self.calcRFphases(RFcavity)
        
        for i, cname in enumerate(RFcavity):
            turns  = data[i][0]
            phases = data[i][1]
            plt.plot(turns, phases, linewidth=3, label=cname, **kwargs)
        plt.xlabel("Turn number")
        plt.ylabel("RF phase [deg]")
        plt.legend(loc=0)
        
        return plt
