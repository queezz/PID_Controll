import sys
sys.path.append("./components/")
import time
import datetime
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import numpy as np

TEST = False
try:
    import RPi.GPIO as GPIO
    import AIO
except:
    print("no RPi.GPIO or AIO")
    TEST = True

class Worker(QtCore.QObject):

    sigStep = QtCore.pyqtSignal(str, list, list)
    sigDone = QtCore.pyqtSignal(int, str)
    sigMsg = QtCore.pyqtSignal(str)

    def __init__(self, id: int, type: str, app: QtGui.QApplication):
        super().__init__()
        self.__id = id
        self.type = type
        self.__app = app
        self.__abort = False
        self.xdata = []
        self.ydata = []

    @QtCore.pyqtSlot()
    def temperatureWork(self):
        self.__setThread()
        if TEST:
            self.__test()
        else:
            pass


    @QtCore.pyqtSlot()
    def pressure1Work(self):
        self.__setThread()
        if TEST:
            self.__test()
        else:
            pass

    @QtCore.pyqtSlot()
    def pressure2Work(self):
        self.__setThread()
        if TEST:
            self.__test()
        else:
            pass

    def abort(self):
        self.sigMsg.emit("Worker #{} aborting acquisition".format(self.__id))
        self.__abort = True

    @QtCore.pyqtSlot()
    def __setThread(self):
        threadName = QtCore.QThread.currentThread().objectName()
        threadId = int(QtCore.QThread.currentThreadId())

        self.sigMsg.emit(
            "Running worker #{} from thread '{}' (#{})".format(self.__id, threadName, threadId)
        )

    @QtCore.pyqtSlot()
    def __test(self):
        startTime = datetime.datetime.now()
        step = 0
        while not (self.__abort):
            time.sleep(0.01)
            currentTime = datetime.datetime.now()
            deltaSeconds = (currentTime - startTime).total_seconds()
            self.xdata.append(deltaSeconds)

            # TODO: 実際のdata追加
            self.ydata.append(np.random.normal()*10)

            if step%10 == 0:
                self.sigStep.emit(self.type, self.xdata, self.ydata)
                self.xdata = []
                self.ydata = []
            step += 1
            # 待機状態にする
            self.__app.processEvents()

        else:
            self.sigMsg.emit(
                "Worker #{} aborting work at step {}".format(self.__id, step)
            )
        self.sigDone.emit(self.__id, self.type)
        return
