import sys
import numpy as np
import pandas as pd
from pyqtgraph.Qt import QtCore, QtGui

from mainView import UIWindow
from worker import Worker

""" debug """
# def trap_exc_during_debug(*args):
#     print(args)

# sys.excepthook = trap_exc_during_debug

# must inherit QtCore.QObject in order to use 'connect'
class MainWidget(QtCore.QObject, UIWindow):
    THREADS_NAME = ["Temperature", "Pressure1", "Pressure2"]
    DEFAULT_TEMPERATURE = 700

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

        self.tData = np.zeros(shape=(301, 2))
        self.p1Data = np.zeros(shape=(301, 2))
        self.p2Data = np.zeros(shape=(301, 2))

        self.valueTPlot = self.graph.temperaturePl.plot(pen='#6ac600')
        self.valueP1Plot = self.graph.pressurePl1.plot(pen='#6ac600')
        self.valueP2Plot = self.graph.pressurePl2.plot(pen='#6ac600')

        self.showMain()

    def startThreads(self):
        self.logDock.log.append("starting {} threads".format(len(self.THREADS_NAME)))

        self.controlDock.startBtn.setDisabled(True)
        self.controlDock.stopBtn.setEnabled(True)
        self.registerDock.registerBtn.setDisabled(True)

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
            worker = Worker(index, name, self.__app, self.__temperature)
            thread = QtCore.QThread()
            thread.setObjectName("thread_" + str(index))

            self.__threads.append((thread, worker))
            worker.moveToThread(thread)

            worker.sigStep.connect(self.onWorkerStep)
            worker.sigDone.connect(self.onWorkerDone)
            worker.sigMsg.connect(self.logDock.log.append)

            self.sigAbortWorkers.connect(worker.abort)

            df = pd.DataFrame(np.zeros(shape=(1, 2)))
            # TODO: set temperature in header
            df.to_csv(
                "./data/{}/out_{}.csv".format(name, self.__stepCount),
                header=["Time", "{}".format(name)],
                index=False
            )

            self.controlDock.setStatus(name, True)

            thread.started.connect(worker.work)
            thread.start()

    @QtCore.pyqtSlot(str, np.ndarray)
    def onWorkerStep(self, threadtype: str, xyResult: np.ndarray, average: float):
        txt = """<font size = 20 color = "#d1451b">{:.2f}</font>""".format(average)

        if threadtype == "Temperature":
            self.controlDock.valueTBw.setText(txt)
            self.tData = self.__setStepData(self.tData, xyResult, threadtype)
            self.valueTPlot.setData(self.tData[:, 0], self.tData[:, 1])
            return
        elif threadtype == "Pressure1":
            self.controlDock.valueP1Bw.setText(txt)
            self.p1Data = self.__setStepData(self.p1Data, xyResult, threadtype)
            self.valueP1Plot.setData(self.p1Data[:, 0], self.p1Data[:, 1])
            return
        elif threadtype == "Pressure2":
            self.controlDock.valueP2Bw.setText(txt)
            self.p2Data = self.__setStepData(self.p2Data, xyResult, threadtype)
            self.valueP2Plot.setData(self.p2Data[:, 0], self.p2Data[:, 1])
            return
        else:
            return

    def __setStepData(self, data: np.ndarray, xyResult: np.ndarray, threadtype: str):
        # self.__save(xyResult, threadtype)
        data = np.roll(data, -10)
        data = np.concatenate((data[:-10, :], np.array(xyResult)))

        return data

    def __save(self, data: np.ndarray, threadtype: str):
        df = pd.DataFrame(data)
        df.to_csv(
            "./data/{}/out_{}.csv".format(threadtype, self.__stepCount),
            mode="a",
            header=False,
            index=False
        )

    @QtCore.pyqtSlot(int, str)
    def onWorkerDone(self, workerId: int, threadtype: str):
        self.logDock.log.append("Worker #{} done".format(workerId))
        self.logDock.progress.append("-- Signal {} STOPPED".format(workerId))
        self.__workers_done += 1

        if threadtype == "Temperature":
            self.tData = np.zeros(shape=(301, 2))
        elif threadtype == "Pressure1":
            self.p1Data = np.zeros(shape=(301, 2))
        elif threadtype == "Pressure2":
            self.p2Data = np.zeros(shape=(301, 2))
        else:
            return

        self.controlDock.setStatus(threadtype, False)

        if self.__workers_done == len(self.THREADS_NAME):
            # self.abortWorkers()   # not necessary
            self.logDock.log.append("No more workers active")
            self.controlDock.startBtn.setEnabled(True)
            self.controlDock.stopBtn.setDisabled(True)
            self.registerDock.registerBtn.setEnabled(True)

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

if __name__ == "__main__":
    app = QtGui.QApplication([])
    widget = MainWidget(app)

    sys.exit(app.exec_())
