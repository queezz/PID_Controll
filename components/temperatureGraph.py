import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import DockArea,Dock
import numpy as np

class TemperatureGraph(pg.GraphicsLayoutWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("graph")
        self.pl = self.addPlot()
        self.pl.setLabel('left', "Temperature", units='K')
        self.pl.setLabel('bottom', "Time", units='msec')


    # def __plot(self):


if __name__ == '__main__':
    pass
