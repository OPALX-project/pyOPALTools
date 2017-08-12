# 18. May, 2017, https://pythonspot.com/en/pyqt5-horizontal-layout/
# 18. May, 2017, https://pythonspot.com/en/pyqt5-matplotlib/
# 18. May, 2017, https://www.tutorialspoint.com/pyqt/pyqt_qpushbutton_widget.htm

#from PyQt5.QtCore import * #QApplication, QWidget
#from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os

from Plotter import *
from SDDSParser import *
from SDDSPlotter import *
from Canvas import *
from enum import IntEnum
import matplotlib.ticker as ticker


class PH5MainFrame(QMainWindow):
    
    class PlotterType(IntEnum):
        SDDS = 0
    
    def __init__(self, parent=None):
        super(PH5MainFrame, self).__init__(parent)
        
        self.resize(1100, 800)
        self.move(200, 200)
        self.setWindowTitle('pyH5root')   
        
        self._statfiles = []
        self._plotter = [SDDSPlotter()]
        self._yvars = []
        
        self._initMenuBar()
        self._initRightFrame()
        self._initCentralFrame()
        
        self.show()
    
    def _initMenuBar(self):
        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu('File')
        #editMenu = mainMenu.addMenu('Edit')
        #viewMenu = mainMenu.addMenu('View')
        #searchMenu = mainMenu.addMenu('Search')
        #toolsMenu = mainMenu.addMenu('Tools')
        #helpMenu = mainMenu.addMenu('Help')
        optionMenu = mainMenu.addMenu('Options')
        
        # File menus
        loadSDDSButton = QAction('Load SDDS file', self)
        loadSDDSButton.setShortcut('Ctrl+S')
        loadSDDSButton.setStatusTip('Load an OPAL statistic file')
        loadSDDSButton.triggered.connect(self._loadSDDS)
        fileMenu.addAction(loadSDDSButton)
        
        exitButton = QAction('Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)
        
        # Option menus
        self._action_logx = QAction('Logarithmic x-axis', self, checkable=True)
        self._action_logx.setStatusTip('Plot with logarithmic x-axis')
        self._action_logx.triggered.connect(self.applyOptions)
        optionMenu.addAction(self._action_logx)
        
        self._action_logy = QAction('Logarithmic y-axis', self, checkable=True)
        self._action_logy.setStatusTip('Plot with logarithmic y-axis')
        self._action_logy.triggered.connect(self.applyOptions)
        optionMenu.addAction(self._action_logy)
        
        self._action_grid = QAction('Grid', self, checkable=True)
        self._action_grid.setStatusTip('Plot with grid')
        self._action_grid.triggered.connect(self.applyOptions)
        optionMenu.addAction(self._action_grid)
        
        self._action_scix = QAction('Scientific x-ticks', self, checkable=True)
        self._action_scix.setStatusTip('Plot with scientific ticks for the x-axis')
        self._action_scix.triggered.connect(self.applyOptions)
        optionMenu.addAction(self._action_scix)
        
        self._action_sciy = QAction('Scientific y-ticks', self, checkable=True)
        self._action_sciy.setStatusTip('Plot with scientific ticks for the y-axis')
        self._action_sciy.triggered.connect(self.applyOptions)
        optionMenu.addAction(self._action_sciy)
        
    
    def _initRightFrame(self):
        
        layout = QVBoxLayout()
        
        self._listSDDS = QListWidget(self)
        self._listSDDS.resize(250, 300)
        self._listSDDS.move(10, 35)
        self._listSDDS.show()
        layout.addWidget(self._listSDDS)
        
        self._xcombobox = QComboBox(self)
        self._xcombobox.move(10, 345)
        self._xcombobox.setFixedWidth(120)
        self._xcombobox.show()
        
        self._ycombobox = QComboBox(self)
        self._ycombobox.move(135, 345)
        self._ycombobox.setFixedWidth(120)
        self._ycombobox.show()
        
        self.plotButton = QPushButton("Plot", self)
        self.plotButton.setCheckable(True)
        self.plotButton.clicked.connect(self._plot)
        self.plotButton.move(10, 385 + 10)
        layout.addWidget(self.plotButton)
        
        self.overlayCheckBox = QCheckBox("Overlay Plots", self)
        self.overlayCheckBox.setCheckable(True)
        self.overlayCheckBox.setFixedWidth(120)
        self.overlayCheckBox.move(115, 385 + 10)
        self.overlayCheckBox.clicked.connect(self._copyYvar)
        layout.addWidget(self.overlayCheckBox)
        
        self.saveButton = QPushButton("Save", self)
        self.saveButton.setCheckable(True)
        self.saveButton.setEnabled(False)
        self.saveButton.clicked.connect(self._savePlot)
        self.saveButton.move(10, 385 + 10 + 35)
        layout.addWidget(self.saveButton)
        
    
    def _initCentralFrame(self):
        self._canvas = Canvas(self, width=8, height=6.5)
        self._canvas.move(275, 35)
    
    
    def _loadSDDS(self):
        
        filetypes = "SDDS Files (*.stat);;SDDS Files (*.lbal);;SDDS Files (*.mem);;All Files (*)"
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self,
                                                  "QFileDialog.getOpenFileName()",
                                                  "",
                                                  filetypes,
                                                  options=options)
        if filename:
            self._statfiles.append(filename)
            
            # 3. June 2017
            # https://stackoverflow.com/questions/26199374/add-qwidget-to-qlistwidget
            item = QListWidgetItem() 
            self._listSDDS.addItem(item)
            self._listSDDS.setItemWidget(item, QCheckBox(os.path.basename(filename)))
            
            if str(self._ycombobox.currentText()) == '':
                parser = SDDSParser()
                parser.parse(self._statfiles[0])
                varnames = parser.getVariables()
                for name in varnames:
                    self._xcombobox.addItem(name)
                    self._ycombobox.addItem(name)
            
                self._xcombobox.model().sort(0)
                self._ycombobox.model().sort(0)
    
    
    def _plot(self):
        self.plotButton.toggle()
        
        entrySDDS = self._fillSDDS()
        
        if entrySDDS:
            idx = self.PlotterType.SDDS
            
            self._canvas.clear()
            self._canvas.show()
            
            if not self.overlayCheckBox.isChecked():
                self._yvars.clear()
                
                
            self._plotter[idx].clear()
            
            xvar = str(self._xcombobox.currentText())
            self._yvars.append( str(self._ycombobox.currentText()) )
            
            for i in entrySDDS:
                self._plotter[idx].addDataset(self._statfiles[i], SDDSParser())
            
            self._plotter[idx].plot(xvar, self._yvars, self._canvas)
            
            self._canvas.show()
            
            self.saveButton.setEnabled(True)
            
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText("Cannot plot.")
            msg.setDetailedText("Either you selected no files or " + \
                                "you selected two different file types"
                                )
            msg.setWindowTitle("Plotting Information")
            msg.show()
    

    def _savePlot(self):
        
        self.saveButton.toggle()
        xvar = str(self._xcombobox.currentText())
        yvar = str(self._ycombobox.currentText())
        
        formats = plt.gcf().canvas.get_supported_filetypes()
        
        nItems = len( formats )
        
        extension = []
        description = ""
        i = 0
        for ext, desc in formats.items():
            extension.append('.' + ext)
            description += desc + ' (*.' + ext + ')'
            
            if i < nItems - 1:
                description += ';;'
            i += 1
        
        # empty string if nothing plotted
        plotname = ''
        if xvar:
            plotname = xvar + '_' + yvar
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, filetype = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()",
                                                         plotname,"All Files (*);;" + description,
                                                         options=options)
        
        # 7. July 2017
        # https://stackoverflow.com/questions/14849293/python-find-index-postion-in-list-based-of-partial-string
        idx = [idx for idx, s in enumerate(extension) if s in filetype]
        
        # if user didn't save --> quit
        if not filename:
            return
        
        # catch case where user add extension by hand
        # to the filename
        if idx:
            self._canvas.save(filename, extension[idx[0]])
        else:
            self._canvas.save(filename)
    
    
    def _copyYvar(self):
        self._yvars.clear()
        if self.overlayCheckBox.isChecked():
            self._plot()
            self.plotButton.toggle()
    
    
    def _fillSDDS(self):
        entrySDDS = []
        # check what is selected
        for r in range(0, self._listSDDS.count()):
            item = self._listSDDS.item(r)
            checkbox = self._listSDDS.itemWidget(item)
            if checkbox.isChecked():
                entrySDDS.append(r)
        return entrySDDS
    
    
    def applyOptions(self):
        
        axes = self._canvas.getAxes()
        
        xscale = 'linear' 
        if self._action_logx.isChecked():
            xscale = 'log'
        axes.set_xscale(xscale)
        
        yscale = 'linear'
        if self._action_logy.isChecked():
            yscale = 'log'
        axes.set_yscale(yscale)
        
        xstyle = 'plain'
        if self._action_scix.isChecked():
            xstyle = 'scientific'
        self._setAxisStyle(xstyle, 'x')
        
        ystyle = 'plain'
        if self._action_sciy.isChecked():
            ystyle = 'scientific'
        self._setAxisStyle(ystyle, 'y')
        
        axes.grid(self._action_grid.isChecked())
    
    
    def _setAxisStyle(self, style, axis):
        axes = self._canvas.getAxes()
        
        if axis == 'y':
            axes.yaxis.set_major_formatter(ticker.ScalarFormatter())
        else:
            axes.xaxis.set_major_formatter(ticker.ScalarFormatter())
        
        axes.ticklabel_format(style=style, axis=axis,
                              scilimits=(0,0))
