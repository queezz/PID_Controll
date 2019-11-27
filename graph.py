import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

class UIWindow(object):

    def __init__(self, MainWindow):
        super().__init__()
        self.MainWindow = MainWindow
        # TODO: set Size
        self.MainWindow.setGeometry(100, 100, 600, 500)
        self.MainWindow.setObjectName("Monitor")
        self.MainWindow.setWindowTitle("Monitor")

        self.centralWidget = QtGui.QWidget(self.MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.MainWindow.setCentralWidget(self.centralWidget)

        self.graph = pg.GraphicsLayoutWidget()
        self.graph.setObjectName("graph")

        self.startBtn = QtGui.QPushButton("start", self.centralWidget)
        self.stopBtn = QtGui.QPushButton("stop", self.centralWidget)

        self.__is_running = True

        self.__setLayout()
        self.__setTimer()
        self.__setGraph()
        self.__setBtn()

        self.__plotGraph()

        self.MainWindow.show()

    # MARK: Set
    def __setLayout(self):
        self.layout = QtGui.QGridLayout(self.centralWidget)
        self.layout.setObjectName("layout")

        self.layout.addWidget(self.startBtn, 0, 8)
        self.layout.addWidget(self.stopBtn, 1, 8)
        self.layout.addWidget(self.graph, 0, 0, 5, 7)

    def __setTimer(self):
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.__update)

    def __setGraph(self):
        print("msec : data")

        # x axis
        self.ptr = 0
        # y axis
        self.data = np.random.normal(size=300)

        self.pl = self.graph.addPlot()
        self.curve = self.pl.plot(self.data)
        self.pl.setLabel('left', "Temperature", units='K')
        self.pl.setLabel('bottom', "Time", units='msec')

    def __setBtn(self):
        self.startBtn.clicked.connect(self.__onClickedStartStopBtn)
        self.stopBtn.clicked.connect(self.__onClickedStartStopBtn)

    # MARK: Methods
    def __onClickedStartStopBtn(self):
        self.__is_running = not (self.__is_running)

    def __update(self):
        if self.__is_running:
            self.data[:-1] = self.data[1:]
            # TODO:  set data
            self.data[-1] = np.random.normal()

            self.ptr += 1
            self.curve.setData(self.data)
            self.curve.setPos(self.ptr, 0)

            print(str(self.ptr) + " : " + str(self.data[-1]))

    def __plotGraph(self):
        self.timer.start(0)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow =  QtGui.QMainWindow()
    ui = UIWindow(MainWindow)
    sys.exit(app.exec_())
