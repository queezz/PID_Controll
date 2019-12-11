import pyqtgraph as pg

class Graph(pg.GraphicsLayoutWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("graph")

        self.temperaturePl = self.addPlot()
        self.temperaturePl.setLabel('left', "temperature", units='K')
        self.temperaturePl.setLabel('bottom', "time", units='sec')

        self.pressurePl1 = self.addPlot(row=1, col=0)
        self.pressurePl1.setLabel('left', "pressure1", units='Torr')
        self.pressurePl1.setLabel('bottom', "time", units='sec')

        self.pressurePl2 = self.addPlot(row=2, col=0)
        self.pressurePl2.setLabel('left', "pressure2", units='Torr')
        self.pressurePl2.setLabel('bottom', "time", units='sec')

if __name__ == '__main__':
    pass
