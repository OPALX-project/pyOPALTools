from pyH5root.Plotter import *
import pyH5root.SDDSParser as statparser


class SDDSPlotter(Plotter):
    
    def __init__(self):
        super(SDDSPlotter, self).__init__()
    
    
    def plot(self, xvar, yvars, canvas):
        
        axes = canvas.getAxes()
        
        for i in range(0, len( self._parser )):
            for j in range(0, len(yvars)):
            
                xdata = self._parser[i].getDataOfVariable(xvar)
                ydata = self._parser[i].getDataOfVariable(yvars[j])
            
                xunit = self._parser[i].getUnitOfVariable(xvar)
                yunit = self._parser[i].getUnitOfVariable(yvars[j])
                
                if len(yvars) > 1:
                    canvas.addLegend(self._basenames[i] + ' - ' + yvars[j]) 
                else:
                    canvas.addLegend(self._basenames[i])
                #ax.tight_layout()
                axes.plot(xdata, ydata)
        
        yvar = yvars[0]
        if len(yvars) > 1:
            yvar = self.longest_common_substring(yvars[0], yvars[1])
        
        axes.set_xlabel(xvar + ' [' + xunit + ']')
        axes.set_ylabel(yvar + ' [' + yunit + ']')
    
    def lineplot(self, canvas):
        raise RuntimeError("Lineplot not implemented.")
