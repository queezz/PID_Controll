import time, datetime, math
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
from typing import Callable
from thermocouple import calcTemp
from customTypes import ThreadType, ScaleSize

TEST = False
try:
    import RPi.GPIO as GPIO
    import AIO
except:
    print("no RPi.GPIO or AIO")
    TEST = True

# must inherit QtCore.QObject in order to use 'connect'
class Worker(QtCore.QObject):

    sigStep = QtCore.pyqtSignal(np.ndarray, np.ndarray, float, ThreadType)
    sigDone = QtCore.pyqtSignal(int, ThreadType)
    sigMsg = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def setWorker(self, id: int, ttype: ThreadType, app: QtGui.QApplication, startTime: datetime, value: int, scale: ScaleSize):
        self.__id = id
        self.__ttype = ttype
        self.__app = app
        self.__abort = False
        self.__startTime = startTime
        self.__presetTemp = value
        self.__scaleSize = scale
        self.__rawData = np.zeros(shape=(10, 3))
        self.__calcData = np.zeros(shape=(10, 3))

    # MARK: - Getters
    def getThreadType(self):
        return self.__ttype

    def getScaleSize(self):
        return self.__scaleSize

    # MARK: - Setters
    def setScaleSize(self, scale: ScaleSize):
        self.__scaleSize = scale
        return

    def setPresetTemp(self, newTemp: int):
        self.__presetTemp = newTemp
        return

    # MARK: - Methods
    @QtCore.pyqtSlot()
    def work(self):
        self.__setThread()
        if TEST:
            self.__test()
        else:
            if self.__ttype == ThreadType.PRASMA:
                self.__test()
            elif self.__ttype == ThreadType.TEMPERATURE:
                self.__plotTemp()
            elif self.__ttype == ThreadType.PRESSURE1:
                self.__plotPress1()
            elif self.__ttype == ThreadType.PRESSURE2:
                self.__test()
            else:
                return

    def __setThread(self):
        threadName = QtCore.QThread.currentThread().objectName()
        threadId = int(QtCore.QThread.currentThreadId())

        self.sigMsg.emit(
            "Running worker #{} from thread '{}' (#{})".format(self.__id, threadName, threadId)
        )

    @QtCore.pyqtSlot()
    def abort(self):
        self.sigMsg.emit("Worker #{} aborting acquisition".format(self.__id))
        self.__abort = True

    # MARK: - Plot
    def __plotPrasma(self):
        # TODO: calc, pinId(plus, minus), control
        self.__plot(3, 4, self.__calcTest, self.__controlCur)

    def __plotTemp(self):
        self.__plot(0, 17, AIO.AIO_32_0RA_IRC.PGA.PGA_1_2544V, calcTemp, self.__controlTemp)

    def __plotPress1(self):
        # TODO: calc
        self.__plot(1, 18, AIO.AIO_32_0RA_IRC.PGA.PGA_10_0352V, self.__calcTest)

    def __plotPress2(self):
        # TODO: calc, pinId
        self.__plot(2, 5, self.__calcTest)

    def __plot(self, pId: int, mId: int, fscale: int, calc: Callable[[float], float], control: Callable[[float, int], int]=None):
        aio = AIO.AIO_32_0RA_IRC(0x49, 0x3e)
        if not control is None:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(17, GPIO.OUT)
            controlStep = -1
        totalStep = 0
        step = 0
        aveValue = 0
        while not (self.__abort):
            time.sleep(0.02)
            pvl = aio.analog_read_volt(pId, aio.DataRate.DR_860SPS, pga=fscale)
            mvl = aio.analog_read_volt(mId, aio.DataRate.DR_860SPS, pga=fscale)
            print("{}: {}".format(pId, pvl))
            print("{}: {}".format(mId, mvl))
            voltage = pvl-mvl
            deltaSeconds = (datetime.datetime.now() - self.__startTime).total_seconds()
            value = calc(voltage)

            self.__rawData[step] = [deltaSeconds, voltage, self.__presetTemp]

            if step%9 == 0 and step != 0:
                aveValue = np.mean(self.__rawData[:, 1], dtype=float)
                if not control is None:
                    controlStep = control(aveValue, controlStep)
                self.__calcData = np.array(list(map(lambda x: [x[0], calc(x[1]), x[2]], self.__rawData)))
                self.sigStep.emit(self.__rawData, self.__calcData, calc(aveValue), self.__ttype)
                self.__rawData = np.zeros(shape=(10, 3))
                self.__calcData = np.zeros(shape=(10, 3))
                step = 0
            else:
                step += 1
            totalStep += 1

            if not control is None:
                GPIO.output(17, controlStep > 0)
                controlStep -= 1

            self.__app.processEvents()
        else:
            if self.__rawData[step][0] == 0.0:
                step -= 1
            if step > -1:
                self.__calcData = np.array(list(map(lambda x: [x[0], calc(x[1]), x[2]], self.__rawData)))
                self.sigStep.emit(self.__rawData[:step+1, :], self.__calcData, calc(self.__rawData[step][1]), self.__ttype)
            self.sigMsg.emit(
                "Worker #{} aborting work at step {}".format(self.__id, totalStep)
            )
            if not control is None:
                GPIO.cleanup()
        self.sigDone.emit(self.__id, self.__ttype)
        return

    # MARK: - Control
    def __controlTemp(self, aveTemp: float, steps: int):
        if steps <= 0:
            d = self.__presetTemp - aveTemp
            if d <= 2:
                return -1
            elif d >= 10:
                return int(d*10)
            else:
                return int(d+1)
        else:
            return steps

    def __controlCur(self, aveCur: float, steps: int):
        pass

    # MARK: - Test
    def __test(self):
        totalStep = 0
        step = 0
        while not (self.__abort):
            time.sleep(0.01)
            deltaSeconds = (datetime.datetime.now() - self.__startTime).total_seconds()
            self.__rawData[step] = [deltaSeconds, np.random.normal(), self.__presetTemp]

            if step%9 == 0 and step != 0:
                average = np.mean(self.__rawData[:, 1], dtype=float)
                self.__calcData = np.array(list(map(lambda x: [x[0], self.__calcTest(x[1]), x[2]], self.__rawData)))
                self.sigStep.emit(self.__rawData, self.__calcData, self.__calcTest(average), self.__ttype)
                self.__rawData = np.zeros(shape=(10, 3))
                self.__calcData = np.zeros(shape=(10, 3))
                step = 0
            else:
                step += 1
            totalStep += 1

            self.__app.processEvents()

        else:
            if self.__rawData[step][0] == 0.0:
                step -= 1
            if step > -1:
                self.__calcData = np.array(list(map(lambda x: [x[0], self.__calcTest(x[1]), x[2]], self.__rawData)))
                self.sigStep.emit(self.__rawData[:step+1, :], self.__calcData[:step+1, :], self.__calcTest(self.__rawData[step][1]), self.__ttype)

            self.sigMsg.emit(
                "Worker #{} aborting work at step {}".format(self.__id, totalStep)
            )
        self.sigDone.emit(self.__id, self.__ttype)
        return

    def __calcTest(self, value: float):
        return value * 3

if __name__ == "__main__":
    pass
