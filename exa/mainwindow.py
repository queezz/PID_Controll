#! /usr/bin/python

"""

"""
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import DockArea,Dock

def gui_setup_spinbox(spbox,val,min,max):
    """set up spinbox value, min and max """
    spbox.setMinimum(min)
    spbox.setMaximum(max)
    spbox.setValue(val)

def html_snc(text,color='red',size=6):
    """ change text color for html output """
    txt = u'<font color = "{c}" size="{s}">{t}</font>'
    return txt.format(c=color,t=text,s=size)

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # Interpret image data as row-major instead of col-major
        pg.setConfigOptions(imageAxisOrder='row-major')
        # == == == == == == == == == == == == == == == == == == == == == == ====
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.tabwidg = QtGui.QTabWidget()
        self.area = DockArea()
        self.area_civ = DockArea()
        self.area_he = DockArea()
        self.area_h = DockArea()
        self.area_cmd = DockArea()
        self.tabwidg.addTab(self.area,"Data")

        MainWindow.setCentralWidget(self.tabwidg)

        MainWindow.setWindowTitle(u'Data Logger')
        MainWindow.resize(1000,900)
        MainWindow.statusBar().showMessage(' ')
        MainWindow.setAcceptDrops(True)
        # == == == == == == == == == == == == == == == == == == == == == == ====
        # DOCs
        # == == == == == == == == == == == == == == == == == == == == == == ====
        self.d1 = Dock("Plots", size=(300,400))
        self.d2 = Dock("field 1", size=(60,20))
        self.d3 = Dock("field 2", size=(60,20))

        #[dd.setAcceptDrops(True) for dd in [self.d1,self.d2,self.d3]]
        self.area.addDock(self.d1, 'top')
        self.area.addDock(self.d2, 'left')
        self.area.addDock(self.d3, 'above',self.d2)

        # == == == == == == == == == == == == == == == == == == == == == == ====
        self.w1 = pg.GraphicsLayoutWidget()
        self.d1.addWidget(self.w1)

        self.p1 = self.w1.addPlot() # spectrum plot

        # == == == == == == == == == == == == == == == == == == == == == == ====
        # Controls
        # == == == == == == == == == == == == == == == == == == == == == == ====
        self.w3 = pg.LayoutWidget()

        self.button_start_threads = QtGui.QPushButton('Start')
        self.button_stop_threads = QtGui.QPushButton('Stop')

        self.value1_bw = QtGui.QTextBrowser()
        self.value1_bw.setMaximumHeight(65)
        self.image_info_bw = QtGui.QTextBrowser()
        self.log = QtGui.QTextEdit()
        self.progress = QtGui.QTextEdit()

        self.w3.addWidget(self.button_start_threads, 1,0)
        self.w3.addWidget(self.button_stop_threads, 1,1)
        self.w3.addWidget(self.value1_bw, 15,0,1,2)
        self.w3.addWidget(self.log,16,0,1,2)
        self.w3.addWidget(self.progress,17,0,1,2)
        #self.w3.addWidget(self.image_info_bw, 20,0,1,2)
        self.d3.addWidget(self.w3)



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())