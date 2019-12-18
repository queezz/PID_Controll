import sys, datetime
import numpy as np
import pandas as pd
from pyqtgraph.Qt import QtCore, QtGui

from mainView import UIWindow
from worker import Worker
from threadType import ThreadType

""" debug """
# def trap_exc_during_debug(*args):
#     print(args)

# sys.excepthook = trap_exc_during_debug

# must inherit QtCore.QObject in order to use 'connect'
class MainWidget(QtCore.QObject, UIWindow):
    DEFAULT_TEMPERATURE = 50
    sigAbortWorkers = QtCore.pyqtSignal()

    def __init__(self, app: QtGui.QApplication):
        super(self.__class__, self).__init__()
        self.__app = app
        self.controlDock.startBtn.clicked.connect(self.startThreads)
        self.controlDock.stopBtn.clicked.connect(self.abortWorkers)
        self.registerDock.registerBtn.clicked.connect(self.registerTemperature)

        self.controlDock.stopBtn.setDisabled(True)
        self.registerDock.setTemperature(self.DEFAULT_TEMPERATURE)

        QtCore.QThread.currentThread().setObjectName("main")

        self.__workers_done = 0
        self.__stepCount = 0
        self.__threads = []
        self.__temperature = self.DEFAULT_TEMPERATURE

        self.tData = np.zeros(shape=(301, 3))
        self.p1Data = np.zeros(shape=(301, 3))
        self.p2Data = np.zeros(shape=(301, 3))

        self.valueTPlot = self.graph.temperaturePl.plot(pen='#6ac600')
        self.valueP1Plot = self.graph.pressurePl1.plot(pen='#6ac600')
        self.valueP2Plot = self.graph.pressurePl2.plot(pen='#6ac600')

        self.tWorker = None
        self.p1Worker = None
        self.p2Worker = None

        self.showMain()

    def startThreads(self):
        self.logDock.log.append("starting {} threads".format(len(ThreadType)))

        self.controlDock.startBtn.setDisabled(True)
        self.controlDock.stopBtn.setEnabled(True)

        self.__workers_done = 0
        self.__stepCount += 1

        try:
            for thread, worker in self.__threads:
                thread.quit()
                thread.wait()
        except:
            pass

        self.__threads = []

        now = datetime.datetime.now()

        for index, tType in enumerate(ThreadType):
            thread = QtCore.QThread()
            thread.setObjectName("thread_" + str(index))
            if tType == ThreadType.TEMPERATURE:
                self.tWorker = Worker(index, tType, self.__app, now, self.__temperature)
                self.setThread(self.tWorker, thread)
            elif tType == ThreadType.PRESSURE1:
                self.p1Worker = Worker(index, tType, self.__app, now, self.__temperature)
                self.setThread(self.p1Worker, thread)
            elif tType == ThreadType.PRESSURE2:
                self.p2Worker = Worker(index, tType, self.__app, now, self.__temperature)
                self.setThread(self.p2Worker, thread)

    def setThread(self, worker: Worker, thread: QtCore.QThread):
        self.__threads.append((thread, worker))
        worker.moveToThread(thread)

        worker.sigStep.connect(self.onWorkerStep)
        worker.sigDone.connect(self.onWorkerDone)
        worker.sigMsg.connect(self.logDock.log.append)
        self.sigAbortWorkers.connect(worker.abort)

        df = pd.DataFrame(np.array([[0, 0, self.DEFAULT_TEMPERATURE]]))
        df.to_csv(
            "./data/{}/out_{}.csv".format(worker.threadType.value, self.__stepCount),
            header=["Time", "{}".format(worker.threadType.value), "PresetTemperature"],
            index=False
        )
        self.controlDock.setStatus(worker.threadType, True)

        thread.started.connect(worker.work)
        thread.start()

    @QtCore.pyqtSlot(np.ndarray, float, ThreadType)
    def onWorkerStep(self, result: np.ndarray, ave: float, threadtype: ThreadType):
        txt = """<font size = 20 color = "#d1451b">{:.2f}</font>""".format(ave)

        if threadtype == ThreadType.TEMPERATURE:
            self.controlDock.valueTBw.setText(txt)
            self.tData = self.__setStepData(self.tData, result, threadtype)
            self.valueTPlot.setData(self.tData[:, 0], self.tData[:, 1])
            return
        elif threadtype == ThreadType.PRESSURE1:
            self.controlDock.valueP1Bw.setText(txt)
            self.p1Data = self.__setStepData(self.p1Data, result, threadtype)
            self.valueP1Plot.setData(self.p1Data[:, 0], self.p1Data[:, 1])
            return
        elif threadtype == ThreadType.PRESSURE2:
            self.controlDock.valueP2Bw.setText(txt)
            self.p2Data = self.__setStepData(self.p2Data, result, threadtype)
            self.valueP2Plot.setData(self.p2Data[:, 0], self.p2Data[:, 1])
            return
        else:
            return

    def __setStepData(self, data: np.ndarray, result: np.ndarray, threadtype: ThreadType):
        if threadtype == ThreadType.TEMPERATURE:
            self.__save(result, threadtype)
        data = np.roll(data, -10, axis=0)
        data = np.concatenate((data[:-10, :], np.array(result)))
        return data

    def __save(self, data: np.ndarray, threadtype: ThreadType):
        df = pd.DataFrame(data)
        df.to_csv(
            "./data/{}/out_{}.csv".format(threadtype.value, self.__stepCount),
            mode="a",
            header=False,
            index=False
        )

    @QtCore.pyqtSlot(int, ThreadType)
    def onWorkerDone(self, workerId: int, threadtype: ThreadType):
        self.logDock.log.append("Worker #{} done".format(workerId))
        self.logDock.progress.append("-- Signal {} STOPPED".format(workerId))
        self.__workers_done += 1

        if threadtype == ThreadType.TEMPERATURE:
            self.tData = np.zeros(shape=(301, 3))
        elif threadtype == ThreadType.PRESSURE1:
            self.p1Data = np.zeros(shape=(301, 3))
        elif threadtype == ThreadType.PRESSURE2:
            self.p2Data = np.zeros(shape=(301, 3))
        else:
            return

        self.controlDock.setStatus(threadtype, False)

        if self.__workers_done == len(ThreadType):
            # self.abortWorkers()   # not necessary
            self.logDock.log.append("No more workers active")
            self.controlDock.startBtn.setEnabled(True)
            self.controlDock.stopBtn.setDisabled(True)

    @QtCore.pyqtSlot()
    def abortWorkers(self):
        self.sigAbortWorkers.emit()
        self.logDock.log.append("Asking each worker to abort")
        for thread, worker in self.__threads:
            thread.quit()
            thread.wait()

        self.logDock.log.append("All threads exited")

    @QtCore.pyqtSlot()
    def registerTemperature(self):
        value = self.registerDock.textField.value()
        self.registerDock.setTemperature(value)
        self.__temperature = value
        self.tWorker.temperature = self.__temperature

if __name__ == "__main__":
    app = QtGui.QApplication([])
    widget = MainWidget(app)

    sys.exit(app.exec_())
