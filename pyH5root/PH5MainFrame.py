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
from FieldParser import *
from FieldPlotter import *
from Canvas import *
from enum import IntEnum


class PH5MainFrame(QMainWindow):
    
    class PlotterType(IntEnum):
        SDDS = 0,
        FIELD = 1
    
    def __init__(self, parent=None):
        super(PH5MainFrame, self).__init__(parent)
        
        self.resize(1100, 800)
        self.move(200, 200)
        self.setWindowTitle('pyH5root')   
        
        self._statfiles = []
        self._fieldfiles = []
        self._plotter = [SDDSPlotter(), FieldPlotter()]
        
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
        
        
        loadSDDSButton = QAction('Load SDDS file', self)
        loadSDDSButton.setShortcut('Ctrl+S')
        loadSDDSButton.setStatusTip('Load an OPAL statistic file')
        loadSDDSButton.triggered.connect(self._loadSDDS)
        fileMenu.addAction(loadSDDSButton)
        
        loadFieldButton = QAction('Load field file', self)
        loadFieldButton.setShortcut('Ctrl+F')
        loadFieldButton.setStatusTip('Load an OPAL field file')
        loadFieldButton.triggered.connect(self._loadFieldFile)
        fileMenu.addAction(loadFieldButton)
        
        exitButton = QAction('Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)
    
    def _initRightFrame(self):
        
        layout = QVBoxLayout()
        
        self._listSDDS = QListWidget(self)
        self._listSDDS.resize(250, 300)
        self._listSDDS.move(10, 35)
        self._listSDDS.show()
        layout.addWidget(self._listSDDS)
        
        self._xcombobox = QComboBox(self)
        self._xcombobox.move(10, 345)
        self._xcombobox.show()
        
        self._ycombobox = QComboBox(self)
        self._ycombobox.move(115, 345)
        self._ycombobox.show()
        
        self._listField = QListWidget(self)
        self._listField.resize(250, 300)
        self._listField.move(10, 385)
        self._listField.show()
        layout.addWidget(self._listField)
        
        self.plotButton = QPushButton("Plot", self)
        self.plotButton.setCheckable(True)
        self.plotButton.clicked.connect(self._plot)
        self.plotButton.move(10, 300 + 385 + 10)
        layout.addWidget(self.plotButton)
        
        self.saveButton = QPushButton("Save", self)
        self.saveButton.setCheckable(True)
        self.saveButton.setEnabled(False)
        self.saveButton.clicked.connect(self._savePlot)
        self.saveButton.move(115, 300 + 385 + 10)
        layout.addWidget(self.saveButton)
        
    
    def _initCentralFrame(self):
        self._canvas = Canvas(self, width=8, height=6.5)
        self._canvas.move(275, 35)
    
    
    def _loadSDDS(self):
        
        filetypes = "SDDS Files (*.stat);;SDDS Files (*.lbal);;All Files (*)"
        
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
    
    
    def _loadFieldFile(self):
        
        potfile = "Potential (*-phi_scalar-*);;"
        rhofile = "Charge density (*-rho_scalar-*);;"
        efile   = "Electric field (*-e_field-*);;"
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self,
                                                  "QFileDialog.getOpenFileName()",
                                                  "", potfile + rhofile + efile + "All Files (*)",
                                                  options=options)
        if filename:
            self._fieldfiles.append(filename)
            item = QListWidgetItem() 
            self._listField.addItem(item)
            self._listField.setItemWidget(item, QCheckBox(os.path.basename(filename)))
    
    
    
    def _plot(self):
        self.plotButton.toggle()
        
        entrySDDS = []
        # check what is selected
        for r in range(0, self._listSDDS.count()):
            item = self._listSDDS.item(r)
            checkbox = self._listSDDS.itemWidget(item)
            if checkbox.isChecked():
                entrySDDS.append(r)
        
        entryField = []
        for r in range(0, self._listField.count()):
            item = self._listField.item(r)
            checkbox = self._listField.itemWidget(item)
            if checkbox.isChecked():
                entryField.append(r)
        
        if entrySDDS and not entryField:
            idx = self.PlotterType.SDDS
            
            self._canvas.clear()
            self._canvas.show()
            self._plotter[idx].clear()
            
            for i in entrySDDS:
                self._plotter[idx].addDataset(self._statfiles[i], SDDSParser())
            
            xvar = str(self._xcombobox.currentText())
            yvar = str(self._ycombobox.currentText())
            
            self._plotter[idx].plot(xvar, yvar, self._canvas)
            
            self._canvas.show()
            
            self.saveButton.setEnabled(True)
            
        elif entryField and not entrySDDS:
            idx = self.PlotterType.FIELD
            self._canvas.clear()
            self._canvas.show()
            self._plotter[idx].clear()
            
            for i in entryField:
                self._plotter[idx].addDataset(self._fieldfiles[i], FieldParser())
            
            self._plotter[idx].lineplot(self._canvas)
            
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
        
        # catch case where user add extension by hand
        # to the filename
        if idx:
            self._canvas.save(filename, extension[idx[0]])
        else:
            self._canvas.save(filename)
