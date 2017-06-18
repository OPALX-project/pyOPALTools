from Plotter import *
import StatFileParser as statparser


class StatPlotter(Plotter):
    
    def __init__(self):
        super(StatPlotter, self).__init__()
    
    
    def plot(self, xvar, yvar, canvas):
        
        axes = canvas.getAxes()
        
        for i in range(0, len( self._parser )):
            
            xdata = self._parser[i].getDataOfVariable(xvar)
            ydata = self._parser[i].getDataOfVariable(yvar)
        
            xunit = self._parser[i].getUnitOfVariable(xvar)
            yunit = self._parser[i].getUnitOfVariable(yvar)
        
            canvas.addLegend(self._basenames[i])
            #ax.tight_layout()
            axes.plot(xdata, ydata)
        
        axes.set_xlabel(xvar + ' [' + xunit + ']')
        axes.set_ylabel(yvar + ' [' + yunit + ']')
        axes.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    
    def lineplot(self, canvas):
        raise RuntimeError("Lineplot not implemented.")
