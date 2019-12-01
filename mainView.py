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
        # self.__setTimer()
        # self.__setGraph()
        # self.__setBtn()

        # self.__plotGraph()

        # self.MainWindow.show()



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

    # def __setTimer(self):
    #     self.timer = pg.QtCore.QTimer()
    #     self.timer.timeout.connect(self.__update)

    # def __setGraph(self):
    #     print("msec : data")

    #     # x axis
    #     self.ptr = 0
    #     # y axis
    #     self.data = np.random.normal(size=300)

    #     self.curve = self.graph.temperaturePl.plot(self.data)

    # def __setBtn(self):
        # self.startBtn.clicked.connect(self.__onClickedStartStopBtn)
        # self.stopBtn.clicked.connect(self.__onClickedStartStopBtn)

    # MARK: Methods
    # def __onClickedStartStopBtn(self):
    #     self.__is_running = not (self.__is_running)

    def __update(self):
        # if self.__is_running:
        self.data[:-1] = self.data[1:]
        # TODO: set data
        self.data[-1] = np.random.normal()

        self.ptr += 1
        self.curve.setData(self.data)
        self.curve.setPos(self.ptr, 0)

        print(str(self.ptr) + " : " + str(self.data[-1]))

    # def __plotGraph(self):
    #     self.timer.start(0)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow =  QtGui.QMainWindow()
    ui = UIWindow()
    ui.MainWindow.show()
    sys.exit(app.exec_())
