import sys
sys.path.append('./components')

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import numpy as np
import pandas as pd
import datetime

from mainView import UIWindow
from worker import Worker

# debug
def trap_exc_during_debug(*args):
    print(args)

sys.excepthook = trap_exc_during_debug

# must inherit QtCore.QObject in order to use 'connect'
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
        self.__stepCount = 0
        self.__threads = []

        self.tData = np.zeros(shape=(301, 2))
        self.p1Data = np.zeros(shape=(301, 2))
        self.p2Data = np.zeros(shape=(301, 2))

        self.valueTPlot = self.graph.temperaturePl.plot(pen='#6ac600')
        self.valueP1Plot = self.graph.pressurePl1.plot(pen='#6ac600')
        self.valueP2Plot = self.graph.pressurePl2.plot(pen='#6ac600')

        self.showMain()

    def startThreads(self):
        self.logDock.log.append("starting {} threads".format(len(self.THREADS_NAME)))

        self.controllDock.startBtn.setDisabled(True)
        self.controllDock.stopBtn.setEnabled(True)

        self.__workers_done = 0
        self.__stepCount += 1

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

            df = pd.DataFrame(np.zeros(shape=(1, 2)))
            df.to_csv(
                "./data/{}/out_{}.csv".format(name, self.__stepCount),
                header=["Time", "{}".format(name)],
                index=False
            )

            thread.started.connect(worker.work)
            thread.start()

    @QtCore.pyqtSlot(str, np.ndarray)
    def onWorkerStep(self, type: str, xyResult: np.ndarray):
        txt = """<font size = 20 color = "#d1451b">{:.2f}</font>""".format(xyResult[-1][1])

        if type == "Temperature":
            self.controllDock.valueTBw.setText(txt)
            self.tData = self.__setStepData(self.tData, xyResult, type)
            self.valueTPlot.setData(self.tData[:, 0], self.tData[:, 1])
            return
        elif type == "Pressure1":
            self.controllDock.valueP1Bw.setText(txt)
            self.p1Data = self.__setStepData(self.p1Data, xyResult, type)
            self.valueP1Plot.setData(self.p1Data[:, 0], self.p1Data[:, 1])
            return
        elif type == "Pressure2":
            self.controllDock.valueP2Bw.setText(txt)
            self.p2Data = self.__setStepData(self.p2Data, xyResult, type)
            self.valueP2Plot.setData(self.p2Data[:, 0], self.p2Data[:, 1])
            return
        else:
            return

    def __setStepData(self, data: np.ndarray, xyResult: np.ndarray, type: str):
        self.__save(xyResult, type)
        data = np.roll(data, -10)
        data = np.concatenate((data[:-10, :], np.array(xyResult)))

        return data

    def __save(self, data: np.ndarray, type: str):
        df = pd.DataFrame(data)
        df.to_csv(
            "./data/{}/out_{}.csv".format(type, self.__stepCount),
            mode="a",
            header=False,
            index=False
        )

    @QtCore.pyqtSlot(int, str)
    def onWorkerDone(self, workerId: int, type: str):
        self.logDock.log.append("Worker #{} done".format(workerId))
        self.logDock.progress.append("-- Signal {} STOPPED".format(workerId))
        self.__workers_done += 1

        if type == "Temperature":
            self.tData = np.zeros(shape=(301, 2))
        elif type == "Pressure1":
            self.p1Data = np.zeros(shape=(301, 2))
        elif type == "Pressure2":
            self.p2Data = np.zeros(shape=(301, 2))
        else:
            return

        if self.__workers_done == len(self.THREADS_NAME):
            # self.abortWorkers()   # not necessary
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