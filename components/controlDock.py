import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from pyqtgraph.dockarea import Dock
from threadType import ThreadType

class ControlDock(Dock):

    def __init__(self):
        super().__init__("Control")
        self.setStretch(30, 10)

        self.widget = pg.LayoutWidget()

        self.startBtn = QtGui.QPushButton("Start All")
        self.stopBtn = QtGui.QPushButton("Stop All")

        self.temperatureLabel = QtGui.QLabel(self.__setLabelFont("Temperature", "#000001"))
        self.temperatureStatus = QtGui.QLabel(self.__setStatusFont(False))
        self.valueTBw = QtGui.QTextBrowser()
        self.valueTBw.setMaximumHeight(65)

        self.pressure1Label = QtGui.QLabel(self.__setLabelFont("Pressure1", "#000001"))
        self.pressure1Status = QtGui.QLabel(self.__setStatusFont(False))
        self.valueP1Bw = QtGui.QTextBrowser()
        self.valueP1Bw.setMaximumHeight(65)

        self.pressure2Label = QtGui.QLabel(self.__setLabelFont("Pressure2", "#000001"))
        self.pressure2Status = QtGui.QLabel(self.__setStatusFont(False))
        self.valueP2Bw = QtGui.QTextBrowser()
        self.valueP2Bw.setMaximumHeight(65)

        self.__setLayout()

    def __setLayout(self):
        self.addWidget(self.widget)

        self.widget.addWidget(self.startBtn, 0, 0)
        self.widget.addWidget(self.stopBtn, 0, 1)

        self.widget.addWidget(self.temperatureLabel, 1, 0)
        self.widget.addWidget(self.temperatureStatus, 1, 1)
        self.widget.addWidget(self.valueTBw, 2, 0, 1, 2)

        self.widget.addWidget(self.pressure1Label, 3, 0)
        self.widget.addWidget(self.pressure1Status, 3, 1)
        self.widget.addWidget(self.valueP1Bw, 4, 0, 1, 2)

        self.widget.addWidget(self.pressure2Label, 5, 0)
        self.widget.addWidget(self.pressure2Status, 5, 1)
        self.widget.addWidget(self.valueP2Bw, 6, 0, 1, 2)

    def __setLabelFont(self, text: str, color: str):
        txt = "<font color={}><h3>{}</h3></font>".format(color, text)
        return txt

    def __setStatusFont(self, active: bool):
        color = "#FF005D" if active else "#002AFF"
        txt = "Active" if active else "InActive"

        return "<font color={}><h3>{}</h3></font>".format(color, txt)

    def setStatus(self, type: ThreadType, active: bool):
        txt = self.__setStatusFont(active)
        if type == ThreadType.TEMPERATURE:
            self.temperatureStatus.setText(txt)
        elif type == ThreadType.PRESSURE1:
            self.pressure1Status.setText(txt)
        elif type == ThreadType.PRESSURE2:
            self.pressure2Status.setText(txt)
        else:
            return

if __name__ == "__main__":
    pass