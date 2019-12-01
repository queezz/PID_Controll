import sys
sys.path.append("./components/")
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import DockArea,Dock
import numpy as np

from controllDock import ControllDock
from logDock import LogDock
from graph import Graph

class UIWindow(object):

    def __init__(self):
        super().__init__()
        pg.setConfigOptions(imageAxisOrder='row-major')

        # MARK: Declaration
        self.MainWindow = QtGui.QMainWindow()
        self.tabwidg = QtGui.QTabWidget()
        self.area = DockArea()
        self.plotDock = Dock("Plots", size=(300, 400))
        self.controllDock = ControllDock()
        self.logDock = LogDock()
        self.graph = Graph()

        self.MainWindow.setGeometry(100, 100, 1000, 900)
        self.MainWindow.setObjectName("Monitor")
        self.MainWindow.setWindowTitle("Data Logger")
        self.MainWindow.statusBar().showMessage('')
        self.MainWindow.setAcceptDrops(True)

        # self.__is_running = True

        self.__setLayout()

    # MARK: Set
    def __setLayout(self):
        self.MainWindow.setCentralWidget(self.tabwidg)
        self.tabwidg.addTab(self.area, "Data")

        self.area.addDock(self.plotDock, "top")
        self.area.addDock(self.controllDock, "left")
        self.area.addDock(self.logDock, "bottom")

        self.plotDock.addWidget(self.graph)

    def showMain(self):
        self.MainWindow.show()

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow =  QtGui.QMainWindow()
    ui = UIWindow()
    ui.showMain()
    sys.exit(app.exec_())
