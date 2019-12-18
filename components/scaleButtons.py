import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.dockarea import Dock
from customTypes import ScaleSize

class ScaleButtons(pg.LayoutWidget):

    def __init__(self):
        super().__init__()
        self.scaleLabel = QtGui.QLabel(self.__setLabelFont("Scale:", "#000001"))
        self.selectBtn = QtGui.QComboBox()
        self.__setSelect()
        self.__setLayout()

    def __setLayout(self):
        self.addWidget(self.scaleLabel, 0, 0, 1, 1)
        self.addWidget(self.selectBtn, 1, 0, 1, 1)

    def __setSelect(self):
        self.selectBtn.addItem("Small")
        self.selectBtn.addItem("Medium")
        self.selectBtn.addItem("Large")
        self.selectBtn.addItem("Full")

    def __setLabelFont(self, text: str, color: str):
        txt = "<font color={}><h4>{}</h4></font>".format(color, text)
        return txt

if __name__ == "__main__":
    pass