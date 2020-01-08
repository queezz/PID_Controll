import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from pyqtgraph.dockarea import Dock

class RegisterDock(Dock):

    def __init__(self):
        super().__init__("Register")
        self.widget = pg.LayoutWidget()

        self.registerLabel = QtGui.QLabel(self.__setLabelFont("Temperature: ", "#000001"))
        self.tempBw = QtGui.QTextBrowser()
        self.tempBw.setMaximumHeight(40)
        self.textField = QtGui.QSpinBox()
        self.textField.setMinimum(0)
        self.textField.setMaximum(600)
        self.textField.setSuffix(" ℃")
        self.textField.setSingleStep(10)
        self.registerBtn = QtGui.QPushButton("register")
        self.upButton= QtGui.QPushButton("Up")
        self.downButton= QtGui.QPushButton("Down")
        self.__setLayout()

    def __setLayout(self):
        self.addWidget(self.widget)

        self.widget.addWidget(self.registerLabel, 0, 0)
        self.widget.addWidget(self.tempBw, 0, 1)
        self.widget.addWidget(self.registerBtn, 0, 2)
        self.widget.addWidget(self.textField, 1, 0)
        self.widget.addWidget(self.upButton, 1, 1)
        self.widget.addWidget(self.downButton, 1, 2)
        self.textField.setStyleSheet("QSpinBox::up-button { width: 25px; }\n"
            "QSpinBox::down-button { width: 27px;}")
        self.upButton.clicked.connect(self.__onTouchUpBtn)
        self.downButton.clicked.connect(self.__onTouchDownBtn)

    def __setLabelFont(self, text: str, color: str):
        txt = "<font color={}><h4>{}</h4></font>".format(color, text)
        return txt

    """ QSpinBox """
    def __onTouchUpBtn(self):
        cur = self.textField.value()
        self.textField.setValue(cur+10)

    def __onTouchDownBtn(self):
        cur = self.textField.value()
        self.textField.setValue(cur-10)

    """ set temperature """
    def setTemp(self, temperature: int):
        self.tempBw.setText("""<font size=4 color="#d1451b">{} ℃</font>""".format(temperature))
        self.textField.setValue(temperature)

if __name__ == "__main__":
    pass
