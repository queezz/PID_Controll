import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from pyqtgraph.dockarea import Dock
from customTypes import ThreadType
from components.scaleButtons import ScaleButtons
from components.onoffswitch import MySwitch, OnOffSwitch
from components.analoggaugewidget import AnalogGaugeWidget

class ControlDock(Dock):

    def __init__(self):
        super().__init__("Control")
        self.widget = pg.LayoutWidget()

        self.quitBtn = QtGui.QPushButton("quit")
        self.quitBtn.setStyleSheet(
            "QPushButton {color:#f9ffd9; background:#ed2a0c;}"
            "QPushButton:disabled {color:#8f8f8f; background:#bfbfbf;}"
        )
        self.quitBtn.setFont(QtGui.QFont('serif',16))

        self.valueBw = QtGui.QTextBrowser()
        self.valueBw.setMaximumHeight(110)
        self.scaleBtn = ScaleButtons()

        self.FullNormSW = MySwitch()
        self.OnOffSW = OnOffSwitch()
        self.OnOffSW.setFont(QtGui.QFont('serif',16))
        
        # Analog Gauge to show Temperature
        self.gaugeT = AnalogGaugeWidget()
        self.gaugeT.set_MinValue(0)
        self.gaugeT.set_MaxValue(400)
        self.gaugeT.set_total_scale_angle_size(180)
        self.gaugeT.set_start_scale_angle(180)
        self.gaugeT.set_enable_value_text(False)

        self.__setLayout()

    def __setLayout(self):
        self.addWidget(self.widget)

        self.widget.addWidget(self.OnOffSW, 0, 0)
        self.widget.addWidget(self.quitBtn, 0, 1)

        self.widget.addWidget(self.valueBw, 1, 0,1,2)
        self.widget.addWidget(self.scaleBtn, 2, 1)
        self.widget.addWidget(self.FullNormSW,2,0)

        # Temperature analouge gauge
        self.widget.addWidget(self.gaugeT,3,0)
        
        self.verticalSpacer = QtGui.QSpacerItem(
            0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding
        )
        self.widget.layout.setVerticalSpacing(5)
        self.widget.layout.addItem(self.verticalSpacer)

    def setBwtext(self, ttype: ThreadType, value: float):
        """ Update value in the value browser """
        # Obsolete, exchanged to one browser for all, set-up in main.py
        
        txt = f"""<font size=5 color="#d1451b">{value:.2f}</font>"""
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
