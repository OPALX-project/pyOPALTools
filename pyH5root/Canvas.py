from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class Canvas(FigureCanvas):
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self._fig = Figure(figsize=(width, height), dpi=dpi)
        self._axes = self._fig.add_subplot(111)
        self._fig.patch.set_alpha(0)
        self._fig.set_tight_layout(True)
        FigureCanvas.__init__(self, self._fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        self._legends = []
    
    def addLegend(self, legend):
        self._legends.append(legend)
    
    def show(self):
        self._axes.legend(self._legends, loc='best')
        self.draw()
    
    
    def clear(self):
        self._axes.cla()
        self._legends = []
    
    
    def save(self, filename, format=''):
        # catch case where filename already contains
        # the file extension
        if '.' in filename:
            format = ''
        
        self._fig.savefig(filename=filename + format)
                          #bbox_inches='tight')
    
    
    def getAxes(self):
        return self._axes
