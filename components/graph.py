import pyqtgraph as pg

class Graph(pg.GraphicsLayoutWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("graph")

        self.praPl = self.addPlot(row=0, col=0)
        # TODO: 単位
        self.praPl.setLabel('left', "prasma", units='mA')
        self.praPl.setLabel('bottom', "time", units='sec')

        self.tempPl = self.addPlot(row=1, col=0)
        self.tempPl.setLabel('left', "temperature", units='℃')
        self.tempPl.setLabel('bottom', "time", units='sec')

        self.pres1Pl = self.addPlot(row=2, col=0)
        self.pres1Pl.setLabel('left', "pressure1", units='V')
        self.pres1Pl.setLabel('bottom', "time", units='sec')

        self.pres2Pl = self.addPlot(row=3, col=0)
        self.pres2Pl.setLabel('left', "pressure2", units='Torr')
        self.pres2Pl.setLabel('bottom', "time", units='sec')

if __name__ == '__main__':
    pass
