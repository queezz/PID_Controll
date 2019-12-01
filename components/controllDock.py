import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import Dock

class ControllDock(Dock):

    def __init__(self):
        super().__init__("Controll")
        self.setStretch(60, 20)

        self.widget = pg.LayoutWidget()

        self.startBtn = QtGui.QPushButton("Start All")
        self.stopBtn = QtGui.QPushButton("Stop All")

        self.temperatureLabel = QtGui.QLabel("Temperature")
        self.valueTBw = QtGui.QTextBrowser()
        self.valueTBw.setMaximumHeight(65)


        self.pressure1Label = QtGui.QLabel("Pressure1")
        self.valueP1Bw = QtGui.QTextBrowser()
        self.valueP1Bw.setMaximumHeight(65)

        self.pressure2Label = QtGui.QLabel("Pressure2")
        self.valueP2Bw = QtGui.QTextBrowser()
        self.valueP2Bw.setMaximumHeight(65)

        self.log = QtGui.QTextEdit()
        self.progress = QtGui.QTextEdit()

        self.__setLayout()

    def __setLayout(self):
        self.addWidget(self.widget)

        self.widget.addWidget(self.startBtn, 0, 0)
        self.widget.addWidget(self.stopBtn, 0, 1)

        self.widget.addWidget(self.temperatureLabel, 1, 0, 1, 2)
        self.widget.addWidget(self.valueTBw, 3, 0, 1, 2)

        self.widget.addWidget(self.pressure1Label, 4, 0, 1, 2)
        self.widget.addWidget(self.valueP1Bw, 6, 0, 1, 2)

        self.widget.addWidget(self.pressure2Label, 7, 0, 1, 2)
        self.widget.addWidget(self.valueP2Bw, 9, 0, 1, 2)


if __name__ == "__main__":
    pass