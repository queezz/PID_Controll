import sys, datetime
import numpy as np
import pandas as pd
from pyqtgraph.Qt import QtCore, QtGui

from mainView import UIWindow
from worker import Worker
from customTypes import ThreadType, ScaleSize

""" debug """
# def trap_exc_during_debug(*args):
#     print(args)

# sys.excepthook = trap_exc_during_debug

# must inherit QtCore.QObject in order to use 'connect'
class MainWidget(QtCore.QObject, UIWindow):
    DEFAULT_TEMPERATURE = 0
    sigAbortWorkers = QtCore.pyqtSignal()

    def __init__(self, app: QtGui.QApplication):
        super(self.__class__, self).__init__()
        self.__app = app
        self.__setConnects()
        self.controlDock.stopBtn.setDisabled(True)
        self.registerDock.setTemp(self.DEFAULT_TEMPERATURE)

        QtCore.QThread.currentThread().setObjectName("main")

        self.__workers_done = 0
        self.__threads = []
        self.__temp = self.DEFAULT_TEMPERATURE

        self.praData = None
        self.tData = None
        self.p1Data = None
        self.p2Data = None

        self.graph.removeItem(self.graph.praPl) # remove Plasma current plot
        self.graph.removeItem(self.graph.pres2Pl) # remove P2 plot
        
        self.valuePraPlot = self.graph.praPl.plot(pen='#6ac600')
        self.valueTPlot = self.graph.tempPl.plot(pen='#5999ff')
        self.valueP1Plot = self.graph.pres1Pl.plot(pen='#6ac600')
        #self.valuePxPlot = self.graph.pres1Pl.plot(pen='#5999ff')
        self.valueP2Plot = self.graph.pres1Pl.plot(pen='#5999ff')
        
        self.graph.pres1Pl.setLogMode(y=True)
        self.graph.pres1Pl.setYRange(-8,3,0)
        self.graph.tempPl.setYRange(0,500,0)
        #self.graph.pres1Pl.setDownsampling(auto=True,mode='mean')

        self.prasmaWorker = None
        self.tWorker = None
        self.p1Worker = None
        self.p2Worker = None

        self.showMain()

    def __setConnects(self):
        self.controlDock.startBtn.clicked.connect(self.startThreads)
        self.controlDock.stopBtn.clicked.connect(self.abortThreads)
        self.controlDock.praScaleBtns.selectBtn.activated.connect(
            lambda: self.setScale(self.controlDock.praScaleBtns.selectBtn.currentIndex(), ThreadType.PRASMA)
        )
        self.controlDock.tScaleBtns.selectBtn.activated.connect(
            lambda: self.setScale(self.controlDock.tScaleBtns.selectBtn.currentIndex(), ThreadType.TEMPERATURE)
        )
        self.controlDock.p1ScaleBtns.selectBtn.activated.connect(
            lambda: self.setScale(self.controlDock.p1ScaleBtns.selectBtn.currentIndex(), ThreadType.PRESSURE1)
        )
        self.controlDock.p2ScaleBtns.selectBtn.activated.connect(
            lambda: self.setScale(self.controlDock.p2ScaleBtns.selectBtn.currentIndex(), ThreadType.PRESSURE2)
        )
        self.registerDock.registerBtn.clicked.connect(self.registerTemp)

    # MARK: - Threads
    def startThreads(self):
        self.logDock.log.append("starting {} threads".format(len(ThreadType) - 1)) # TODO: setup

        self.controlDock.startBtn.setDisabled(True)
        self.controlDock.stopBtn.setEnabled(True)

        self.__workers_done = 0

        for thread, worker in self.__threads:
            thread.quit()
            thread.wait()

        self.__threads = []
        # self.prasmaWorker = Worker()
        self.tWorker = Worker()
        self.p1Worker = Worker()
        self.p2Worker = Worker()

        now = datetime.datetime.now()

        print("start threads: {}".format(now))
        self.logDock.progress.append("start threads: {}".format(now))

        for index, worker in enumerate([self.prasmaWorker, self.tWorker, self.p1Worker, self.p2Worker]):
            thread = QtCore.QThread()
            thread.setObjectName("thread_{}".format(index))

            if index == 0:
                scaleButtons = self.controlDock.praScaleBtns
                # TODO: setup
                thread.quit()
                continue
            elif index == 1:
                scaleButtons = self.controlDock.tScaleBtns
            elif index == 2:
                scaleButtons = self.controlDock.p1ScaleBtns
            elif index == 3:
                scaleButtons = self.controlDock.p2ScaleBtns
            else:
                return

            scaleIndex = scaleButtons.selectBtn.currentIndex()
            scale = ScaleSize.getEnum(scaleIndex)
            ttype = ThreadType.getEnum(index)

            worker.setWorker(index, ttype, self.__app, now, self.__temp, scale)
            self.setThread(worker, thread)

    def setThread(self, worker: Worker, thread: QtCore.QThread):
        self.__threads.append((thread, worker))
        worker.moveToThread(thread)

        worker.sigStep.connect(self.onWorkerStep)
        worker.sigDone.connect(self.onWorkerDone)
        worker.sigMsg.connect(self.logDock.log.append)
        self.sigAbortWorkers.connect(worker.abort)
        ttype = worker.getThreadType()

        df = pd.DataFrame(dtype=float, columns=["Time", "{}".format(ttype.value), "PresetTemperature"])
        df.to_csv(
            "./data/{}/out_{:%Y%m%d%H%M%S}.csv".format(ttype.value, worker.getStartTime()),
            index=False
        )
        self.controlDock.setStatus(ttype, True)

        thread.started.connect(worker.work)
        thread.start()

    @QtCore.pyqtSlot(np.ndarray, np.ndarray, float, ThreadType, datetime.datetime)
    def onWorkerStep(self, rawResult: np.ndarray, calcResult: np.ndarray,
                    ave: float, ttype: ThreadType, startTime: datetime.datetime):
        """ collect data on worker step """
        self.controlDock.setBwtext(ttype, ave)

        worker = self.getWorker(ttype)
        scale = worker.getScaleSize().value

        data = self.getData(ttype)
        data = self.__setStepData(data, rawResult, calcResult, ttype, startTime)
        self.setData(ttype, data)

        if ttype == ThreadType.PRASMA:
            self.valuePraPlot.setData(data[scale:, 0], data[scale:, 1])
        elif ttype == ThreadType.TEMPERATURE:
            self.valueTPlot.setData(data[scale:, 0], data[scale:, 1])
            #self.valuePxPlot.setData(data[scale:, 0], data[scale:, 1])
        elif ttype == ThreadType.PRESSURE1:
            self.valueP1Plot.setData(data[scale:, 0], data[scale:, 1])
        elif ttype == ThreadType.PRESSURE2:
            self.valueP2Plot.setData(data[scale:, 0], data[scale:, 1])
        else:
            return
            
    def __setStepData(self, data: np.ndarray, rawResult: np.ndarray,
                      calcResult: np.ndarray, ttype: ThreadType,
                      startTime: datetime.datetime):
        """ Append new data from Worker to main data arrays """
        # TODO: save interval
        self.__save(rawResult, ttype, startTime)
        if data is None:
            data = calcResult
        else:
            data = np.concatenate((data, np.array(calcResult)))
        return data

    """ write csv """
    def __save(self, data: np.ndarray, ttype: ThreadType, startTime: datetime.datetime):
        df = pd.DataFrame(data)
        df.to_csv(
            "./data/{}/out_{:%Y%m%d%H%M%S}.csv".format(ttype.value, startTime),
            mode="a",
            header=False,
            index=False
        )

    @QtCore.pyqtSlot(int, ThreadType)
    def onWorkerDone(self, workerId: int, ttype: ThreadType):
        self.logDock.log.append("Worker #{} done".format(workerId))
        self.logDock.progress.append("-- Signal {} STOPPED".format(workerId))
        self.__workers_done += 1
        self.controlDock.setStatus(ttype, False)
        worker = self.getWorker(ttype)

        self.setData(ttype)

        if self.__workers_done == len(ThreadType) - 1: # TODO: setup
            # self.abortThreads()   # not necessary
            self.logDock.log.append("No more plot workers active")
            self.controlDock.startBtn.setEnabled(True)
            self.controlDock.stopBtn.setDisabled(True)

    @QtCore.pyqtSlot()
    def abortThreads(self):
        self.sigAbortWorkers.emit()
        self.logDock.log.append("Asking each worker to abort")
        for thread, worker in self.__threads:
            thread.quit()
            thread.wait()

        self.logDock.log.append("All threads exited")

    # MARK: - Methods
    @QtCore.pyqtSlot()
    def registerTemp(self):
        value = self.registerDock.temperatureSB.value()
        self.__temp = value
        self.registerDock.setTemp(self.__temp)
        if self.tWorker is not None:
            # self.prasmaWorker.setPresetTemp(self.__temp) # TODO: setup
            self.tWorker.setPresetTemp(self.__temp)
            self.p1Worker.setPresetTemp(self.__temp)
            self.p2Worker.setPresetTemp(self.__temp)

    def setScale(self, index: int, ttype: ThreadType):
        scale = ScaleSize.getEnum(index)
        worker = self.getWorker(ttype)
        worker.setScaleSize(scale)

    def getWorker(self, ttype: ThreadType):
        if self.tWorker is None:
            return
        elif ttype == ThreadType.PRASMA:
            return self.prasmaWorker
        elif ttype == ThreadType.TEMPERATURE:
            return self.tWorker
        elif ttype == ThreadType.PRESSURE1:
            return self.p1Worker
        elif ttype == ThreadType.PRESSURE2:
            return self.p2Worker
        else:
            return

    def getData(self, ttype: ThreadType):
        """ Get data from worker
        """
        if ttype == ThreadType.PRASMA:
            return self.praData
        elif ttype == ThreadType.TEMPERATURE:
            return self.tData
        elif ttype == ThreadType.PRESSURE1:
            return self.p1Data
        elif ttype == ThreadType.PRESSURE2:
            return self.p2Data
        else:
            return

    def setData(self, ttype: ThreadType, data: np.ndarray = None):
        if ttype == ThreadType.PRASMA:
            self.praData = data
        elif ttype == ThreadType.TEMPERATURE:
            self.tData = data
        elif ttype == ThreadType.PRESSURE1:
            self.p1Data = data
        elif ttype == ThreadType.PRESSURE2:
            self.p2Data = data
        else:
            return

if __name__ == "__main__":
    app = QtGui.QApplication([])
    widget = MainWidget(app)

    sys.exit(app.exec_())
