import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from pyqtgraph.dockarea import Dock
from customTypes import ThreadType
from components.scaleButtons import ScaleButtons

class ControlDock(Dock):

    def __init__(self):
        super().__init__("Control")
        self.setStretch(30, 10)

        self.widget = pg.LayoutWidget()

        self.startBtn = QtGui.QPushButton("Start All")
        self.stopBtn = QtGui.QPushButton("Stop All")

        self.prasmaLabel = QtGui.QLabel(self.__setLabelFont("Prasma Current", "#000001"))
        self.prasmaStatus = QtGui.QLabel(self.__setStatusFont(False))
        self.valuePraBw = QtGui.QTextBrowser()
        self.valuePraBw.setMaximumHeight(50)
        self.valuePraBw.setMaximumWidth(130)
        self.praScaleBtns = ScaleButtons()

        self.tempLabel = QtGui.QLabel(self.__setLabelFont("Temperature", "#000001"))
        self.tempStatus = QtGui.QLabel(self.__setStatusFont(False))
        self.valueTBw = QtGui.QTextBrowser()
        self.valueTBw.setMaximumHeight(50)
        self.valueTBw.setMaximumWidth(130)
        self.tScaleBtns = ScaleButtons()

        self.pressure1Label = QtGui.QLabel(self.__setLabelFont("Pressure1", "#000001"))
        self.pressure1Status = QtGui.QLabel(self.__setStatusFont(False))
        self.valueP1Bw = QtGui.QTextBrowser()
        self.valueP1Bw.setMaximumHeight(50)
        self.valueP1Bw.setMaximumWidth(130)
        self.p1ScaleBtns = ScaleButtons()

        self.pressure2Label = QtGui.QLabel(self.__setLabelFont("Pressure2", "#000001"))
        self.pressure2Status = QtGui.QLabel(self.__setStatusFont(False))
        self.valueP2Bw = QtGui.QTextBrowser()
        self.valueP2Bw.setMaximumHeight(50)
        self.valueP2Bw.setMaximumWidth(130)
        self.p2ScaleBtns = ScaleButtons()

        self.__setLayout()

    def __setLayout(self):
        self.addWidget(self.widget)

        self.widget.addWidget(self.startBtn, 0, 0)
        self.widget.addWidget(self.stopBtn, 0, 1)

        self.widget.addWidget(self.prasmaLabel, 1, 0)
        self.widget.addWidget(self.prasmaStatus, 1, 1)
        self.widget.addWidget(self.valuePraBw, 2, 0, 1, 1)
        self.widget.addWidget(self.praScaleBtns, 2, 1, 1, 1)


        self.widget.addWidget(self.tempLabel, 3, 0)
        self.widget.addWidget(self.tempStatus, 3, 1)
        self.widget.addWidget(self.valueTBw, 4, 0, 1, 1)
        self.widget.addWidget(self.tScaleBtns, 4, 1, 1, 1)

        self.widget.addWidget(self.pressure1Label, 5, 0)
        self.widget.addWidget(self.pressure1Status, 5, 1)
        self.widget.addWidget(self.valueP1Bw, 6, 0, 1, 1)
        self.widget.addWidget(self.p1ScaleBtns, 6, 1, 1, 1)

        self.widget.addWidget(self.pressure2Label, 7, 0)
        self.widget.addWidget(self.pressure2Status, 7, 1)
        self.widget.addWidget(self.valueP2Bw, 8, 0, 1, 1)
        self.widget.addWidget(self.p2ScaleBtns, 8, 1, 1, 1)

    def __setLabelFont(self, text: str, color: str):
        txt = "<font color={}><h3>{}</h3></font>".format(color, text)
        return txt

    def __setStatusFont(self, active: bool):
        color = "#FF005D" if active else "#002AFF"
        txt = "Active" if active else "InActive"
        return "<font color={}><h3>{}</h3></font>".format(color, txt)

    def setStatus(self, ttype: ThreadType, active: bool):
        txt = self.__setStatusFont(active)
        if ttype == ThreadType.PRASMA:
            self.prasmaStatus.setText(txt)
        elif ttype == ThreadType.TEMPERATURE:
            self.tempStatus.setText(txt)
        elif ttype == ThreadType.PRESSURE1:
            self.pressure1Status.setText(txt)
        elif ttype == ThreadType.PRESSURE2:
            self.pressure2Status.setText(txt)
        else:
            return
    def setBwtext(self, ttype: ThreadType, value: float):
        txt = """<font size=10 color="#d1451b">{:.2f}</font>""".format(value)
        if ttype == ThreadType.PRASMA:
            self.valuePraBw.setText(txt)
        elif ttype == ThreadType.TEMPERATURE:
            self.valueTBw.setText(txt)
        elif ttype == ThreadType.PRESSURE1:
            self.valueP1Bw.setText(txt)
        elif ttype == ThreadType.PRESSURE2:
            self.valueP2Bw.setText(txt)
        else:
            return

if __name__ == "__main__":
    pass