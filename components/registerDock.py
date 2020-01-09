import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from pyqtgraph import QtCore
from pyqtgraph.dockarea import Dock

DEGREE_SMB = u'\N{DEGREE SIGN}'

class RegisterDock(Dock):

    def __init__(self):
        super().__init__("Membreane Heater")
        self.widget = pg.LayoutWidget()        
        self.tempBw = QtGui.QTextBrowser()        
        self.tempBw.setMinimumSize(QtCore.QSize(80,45))
        self.tempBw.setMaximumHeight(45)
        self.temperatureSB = QtGui.QSpinBox()
        self.temperatureSB.setMinimum(0)
        self.temperatureSB.setMaximum(600)
        self.temperatureSB.setSuffix(f'{DEGREE_SMB}C')
        self.temperatureSB.setMinimumSize(QtCore.QSize(180, 80))
        self.temperatureSB.setSingleStep(10)
        self.temperatureSB.setStyleSheet(
                "QSpinBox::up-button   { width: 60px; }\n"
                "QSpinBox::down-button { width: 60px;}\n"
                "QSpinBox {font: 26pt;}"
        )
        self.registerBtn = QtGui.QPushButton("set")
        self.registerBtn.setMinimumSize(QtCore.QSize(80, 80))
        self.registerBtn.setStyleSheet("font: 26pt")
        self.__setLayout()

    def __setLayout(self):
        self.addWidget(self.widget)

        self.widget.addWidget(self.tempBw, 0, 0,1,2)        
        self.widget.addWidget(self.temperatureSB, 1, 0)
        self.widget.addWidget(self.registerBtn, 1, 1)
        
        self.verticalSpacer = QtGui.QSpacerItem(
            0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding
        )
        self.widget.layout.setVerticalSpacing(0)
        self.widget.layout.addItem(self.verticalSpacer)        

    def setTemp(self, temperature: int):
        htmltag = '<font size=7 color="#d1451b">'
        setpoint = '<font size=5 color="#d1451b">setpoint: </font>'
        self.tempBw.setText(
            f'{setpoint}{htmltag}{temperature} {DEGREE_SMB}C</font>'
        )
        self.temperatureSB.setValue(temperature)

if __name__ == "__main__":
    pass
