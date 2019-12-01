import sys
sys.path.append('./components')

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import numpy as np
import datetime

from mainView import UIWindow
from worker import Worker

def trap_exc_during_debug(*args):
    print(args)

sys.excepthook = trap_exc_during_debug

# QObjectを継承しないとconnectが上手く使えない
class MainWidget(QtCore.QObject, UIWindow):
    THREADS_NAME = ["Temperature", "Pressure1", "Pressure2"]

    sigAbortWorkers = QtCore.pyqtSignal()

    def __init__(self, app: QtGui.QApplication):
        super(self.__class__, self).__init__()
        self.__app = app
        self.controllDock.startBtn.clicked.connect(self.startThreads)
        self.controllDock.stopBtn.clicked.connect(self.abortWorkers)

        self.controllDock.stopBtn.setDisabled(True)

        QtCore.QThread.currentThread().setObjectName("main")

        self.__workers_done = 0
        self.__threads = []

        self.xTData = []
        self.yTData = []

        self.xP1Data = []
        self.yP1Data = []

        self.xP2Data = []
        self.yP2Data = []

        self.valueTPlot = self.graph.temperaturePl.plot(pen='#6ac600')
        self.valueP1Plot = self.graph.pressurePl1.plot(pen='#6ac600')
        self.valueP2Plot = self.graph.pressurePl2.plot(pen='#6ac600')

        self.showMain()

    def startThreads(self):
        self.logDock.log.append("starting {} threads".format(len(self.THREADS_NAME)))

        self.controllDock.startBtn.setDisabled(True)
        self.controllDock.stopBtn.setEnabled(True)

        self.__workers_done = 0

        try:
            for thread, worker in self.__threads:
                thread.quit()
                thread.wait()
        except:
            pass

        self.__threads = []

        for index, name in enumerate(self.THREADS_NAME):
            worker = Worker(index, name, self.__app)
            thread = QtCore.QThread()
            thread.setObjectName("thread_" + str(index))

            self.__threads.append((thread, worker))
            worker.moveToThread(thread)

            worker.sigStep.connect(self.onWorkerStep)
            worker.sigDone.connect(self.onWorkerDone)
            worker.sigMsg.connect(self.logDock.log.append)

            self.sigAbortWorkers.connect(worker.abort)

            if name == "Temperature":
                work = worker.temperatureWork
            elif name == "Pressure1":
                work = worker.pressure1Work
            elif name == "Pressure2":
                work = worker.pressure2Work
            else:
                return
            thread.started.connect(work)
            thread.start()

    @QtCore.pyqtSlot(str, list, list)
    def onWorkerStep(self, type: str, xResult: list, yResult: list):
        txt = """<font size = 20 color = "#d1451b">{:.2f}</font>""".format(yResult[-1])

        if type == "Temperature":
            self.controllDock.valueTBw.setText(txt)
            self.xTData, self.yTData = self.__setStepData(self.xTData, self.yTData, xResult, yResult)
            self.valueTPlot.setData(self.xTData, self.yTData)
            return
        elif type == "Pressure1":
            self.controllDock.valueP1Bw.setText(txt)
            self.xP1Data, self.yP1Data = self.__setStepData(self.xP1Data, self.yP1Data, xResult, yResult)
            self.valueP1Plot.setData(self.xP1Data, self.yP1Data)
            return
        elif type == "Pressure2":
            self.controllDock.valueP2Bw.setText(txt)
            self.xP2Data, self.yP2Data = self.__setStepData(self.xP2Data, self.yP2Data, xResult, yResult)
            self.valueP2Plot.setData(self.xP2Data, self.yP2Data)
            return
        else:
            return

    def __setStepData(self, xdata: list, ydata: list, xResult: list, yResult: list):
        if(len(xdata)==301):
            xdata = np.roll(xdata, -10)
            ydata = np.roll(ydata, -10)

            xdata = np.concatenate((xdata[:-10], np.array(xResult)))
            ydata = np.concatenate((ydata[:-10], np.array(yResult)))
        else:
            xdata = np.concatenate((xdata, np.array(xResult)))
            ydata = np.concatenate((ydata, np.array(yResult)))

        return xdata, ydata

    @QtCore.pyqtSlot(int, str)
    def onWorkerDone(self, workerId: int, type: str):
        self.logDock.log.append("worker #{} done".format(workerId))
        self.logDock.progress.append("-- Signal {} STOPPED".format(workerId))
        self.__workers_done += 1

        if type == "Temperature":
            self.xTData = []
            self.yTData = []
        elif type == "Pressure1":
            self.xP1Data = []
            self.yP1Data = []
        elif type == "Pressure2":
            self.xP2Data = []
            self.yP2Data = []
        else:
            return

        if self.__workers_done == len(self.THREADS_NAME):
            self.abortWorkers()
            self.logDock.log.append("No more workers active")
            self.controllDock.startBtn.setEnabled(True)
            self.controllDock.stopBtn.setDisabled(True)


    @QtCore.pyqtSlot()
    def abortWorkers(self):
        self.sigAbortWorkers.emit()
        self.logDock.log.append("Asking each worker to abort")

        for thread, worker in self.__threads:
            thread.quit()
            thread.wait()

        self.logDock.log.append("All threads exited")

if __name__ == "__main__":
    app = QtGui.QApplication([])
    widget = MainWidget(app)

    sys.exit(app.exec_())