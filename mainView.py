import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import DockArea,Dock
import numpy as np

from components.controllDock import ControllDock
from components.logDock import LogDock
from components.registerDock import RegisterDock
from components.graph import Graph

class UIWindow(object):

    def __init__(self):
        super().__init__()
        pg.setConfigOptions(imageAxisOrder='row-major')

        self.MainWindow = QtGui.QMainWindow()
        self.tabwidg = QtGui.QTabWidget()
        self.area = DockArea()
        self.plotDock = Dock("Plots", size=(300, 400))
        self.controllDock = ControllDock()
        self.logDock = LogDock()
        self.registerDock = RegisterDock()
        self.graph = Graph()

        self.MainWindow.setGeometry(100, 100, 1024, 600)
        self.MainWindow.setObjectName("Monitor")
        self.MainWindow.setWindowTitle("Data Logger")
        self.MainWindow.statusBar().showMessage('')
        self.MainWindow.setAcceptDrops(True)

        self.__setLayout()

    def __setLayout(self):
        self.MainWindow.setCentralWidget(self.tabwidg)
        self.tabwidg.addTab(self.area, "Data")

        self.area.addDock(self.plotDock, "top")
        self.area.addDock(self.controllDock, "left")
        self.area.addDock(self.logDock, "bottom", self.controllDock)
        self.area.addDock(self.registerDock, "above", self.logDock)

        self.plotDock.addWidget(self.graph)

    def showMain(self):
        self.MainWindow.show()

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = UIWindow()
    ui.showMain()
    sys.exit(app.exec_())
