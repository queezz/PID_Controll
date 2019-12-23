import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from pyqtgraph.dockarea import Dock

class RegisterDock(Dock):

    def __init__(self):
        super().__init__("Register")
        self.widget = pg.LayoutWidget()

        self.registerLabel = QtGui.QLabel(self.__setLabelFont("Temperature: ", "#000001"))
        self.tempBw = QtGui.QTextBrowser()
        self.tempBw.setMaximumHeight(55)
        self.textField = QtGui.QSpinBox()
        self.textField.setMinimum(50)
        self.textField.setMaximum(99999)
        self.textField.setSuffix(" ℃")
        self.textField.setSingleStep(50)
        self.registerBtn = QtGui.QPushButton("register")

        self.__setLayout()

    def __setLayout(self):
        self.addWidget(self.widget)

        self.widget.addWidget(self.registerLabel, 0, 0)
        self.widget.addWidget(self.tempBw, 0, 1)
        self.widget.addWidget(self.textField, 1, 0)
        self.widget.addWidget(self.registerBtn, 1, 1)

    def __setLabelFont(self, text: str, color: str):
        txt = "<font color={}><h3>{}</h3></font>".format(color, text)
        return txt

    def setTemp(self, temperature: int):
        self.tempBw.setText("""<font size=6 color="#d1451b">{} ℃</font>""".format(temperature))
        self.textField.setValue(temperature)

if __name__ == "__main__":
    pass