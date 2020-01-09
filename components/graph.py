import pyqtgraph as pg
from pyqtgraph.Qt import QtGui

DEGREE_SMB = u'\N{DEGREE SIGN}'

class Graph(pg.GraphicsLayoutWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("graph")

        self.praPl = self.addPlot(row=0, col=0)
        # TODO: 単位
        self.praPl.setLabel('left', "Ip", units='mA')

        self.tempPl = self.addPlot(row=1, col=0)
        labelStyle = {'color': '#FFF', 'font-size': '14pt'}
        self.tempPl.setLabel('left', "T", units=DEGREE_SMB+'C',**labelStyle)

        self.pres1Pl = self.addPlot(row=2, col=0)
        self.pres1Pl.setLabel('left', "P", units='Torr',**labelStyle)
        self.pres1Pl.setLabel('bottom', "time", units='sec',**labelStyle)

        self.pres2Pl = self.addPlot(row=3, col=0)
        self.pres2Pl.setLabel('left', "pressure2", units='Torr',**labelStyle)
        self.pres2Pl.setLabel('bottom', "time", units='sec')
        
        self.setBackground(background='#25272b')
               
        self.tempPl.getAxis('left').setPen('#fcfcc7')
        font = QtGui.QFont('serif',15)
        self.tempPl.getAxis('left').tickFont = font
        self.pres1Pl.getAxis('left').tickFont = font
        self.pres1Pl.getAxis('bottom').tickFont = font
        self.pres1Pl.getAxis('bottom').setStyle(tickTextOffset = 10)

if __name__ == '__main__':
    pass
