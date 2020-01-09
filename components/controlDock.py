import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from pyqtgraph.dockarea import Dock
from customTypes import ThreadType
from components.scaleButtons import ScaleButtons
from components.onoffswitch import MySwitch 

class ControlDock(Dock):

    def __init__(self):
        super().__init__("Control")
        self.widget = pg.LayoutWidget()

        self.startBtn = QtGui.QPushButton("Start All")
        self.stopBtn = QtGui.QPushButton("Stop All")

        self.valueBw = QtGui.QTextBrowser()
        self.valueBw.setMaximumHeight(85)
        self.scaleBtns = ScaleButtons()

        self.onoffChk = MySwitch()

        self.__setLayout()

    def __setLayout(self):
        self.addWidget(self.widget)

        self.widget.addWidget(self.startBtn, 0, 0)
        self.widget.addWidget(self.stopBtn, 0, 1)
        self.widget.addWidget(self.valueBw, 1, 0,1,2)
        self.widget.addWidget(self.scaleBtns, 2, 0,1,2 )
        self.widget.addWidget(self.onoffChk,3,0)
        
        self.verticalSpacer = QtGui.QSpacerItem(
            0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding
        )
        self.widget.layout.addItem(self.verticalSpacer)

if __name__ == "__main__":
    pass
