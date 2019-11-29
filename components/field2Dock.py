import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import Dock

class Field2Dock(Dock):

    def __init__(self):
        super().__init__("field 1")
        self.setStretch(60, 20)

        self.widget = pg.LayoutWidget()

        self.startBtn = QtGui.QPushButton("Start")
        self.stopBtn = QtGui.QPushButton("Stop")

        self.valueBw = QtGui.QTextBrowser()
        self.valueBw.setMaximumHeight(65)
        self.imageInfoBw = QtGui.QTextBrowser()

        self.__setLayout()

    def __setLayout(self):
        self.addWidget(self.widget)

        self.widget.addWidget(self.startBtn, 1, 0)
        self.widget.addWidget(self.stopBtn, 1, 1)
        self.widget.addWidget(self.valueBw, 15, 0, 1, 2)


if __name__ == "__main__":
    pass