import time, datetime, math
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
from typing import Callable
from customTypes import ThreadType

TEST = False
try:
    import RPi.GPIO as GPIO
    from AIO import AIO_32_0RA_IRC as adc
except:
    print("no RPi.GPIO or AIO")
    TEST = True

# must inherit QtCore.QObject in order to use 'connect'
class Worker(QtCore.QObject):

    sigStep = QtCore.pyqtSignal(np.ndarray, np.ndarray, float, ThreadType, datetime.datetime)
    sigDone = QtCore.pyqtSignal(int, ThreadType)
    sigMsg = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def setWorker(self, id: int, ttype: ThreadType, app: QtGui.QApplication,
                  startTime: datetime.datetime, value: int):
        self.__id = id
        self.__ttype = ttype
        self.__app = app
        self.__abort = False
        self.__startTime = startTime
        self.__presetTemp = value
        self.__rawData = np.zeros(shape=(10, 3))
        self.__calcData = np.zeros(shape=(10, 3))

    # MARK: - Getters
    def getThreadType(self):
        return self.__ttype

    def getStartTime(self):
        return self.__startTime

    # MARK: - Setters
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
            if self.__ttype == ThreadType.PLASMA:
                self.__test()
            elif self.__ttype == ThreadType.TEMPERATURE:
                self.__plotTemp()
            elif self.__ttype == ThreadType.PRESSURE1:
                self.__plotPress1()
            elif self.__ttype == ThreadType.PRESSURE2:
                self.__plotPress2()
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
    def __plotPLASMA(self):
        # TODO: pinId, control
        self.__plot(3, 4, self.__controlCur)

    def __plotTemp(self):
        self.__plot(0, adc.PGA.PGA_1_2544V, self.__controlTemp)

    def __plotPress1(self):
        self.__plot(15, adc.PGA.PGA_10_0352V)

    def __plotPress2(self):
        self.__plot(16, adc.PGA.PGA_10_0352V)

    def __plot(self, pId: int, fscale: int, control: Callable[[float, int], int]=None):
        aio = adc(0x49, 0x3e)
        if not control is None:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.__ttype.getGPIO(), GPIO.OUT)
            controlStep = -1
        totalStep = 0
        step = 0
        while not (self.__abort):
            time.sleep(0.15)
            voltage = aio.analog_read_volt(pId, aio.DataRate.DR_860SPS, pga=fscale)

            deltaSeconds = (datetime.datetime.now() - self.__startTime).total_seconds()
            value = self.__ttype.getCalcValue(voltage)

            #  I do not know why this is needed
            aio.analog_read_volt(15, aio.DataRate.DR_860SPS, pga=2)
            aio.analog_read_volt(16, aio.DataRate.DR_860SPS, pga=2)

            self.__rawData[step] = [deltaSeconds, voltage, self.__presetTemp]

            if step%9 == 0 and step != 0:
                aveValue = np.mean(self.__rawData[:, 1], dtype=float)
                aveValue = self.__ttype.getCalcValue(aveValue)
                if not control is None:
                    controlStep = control(aveValue, controlStep)
                self.__calcData = self.__ttype.getCalcArray(self.__rawData)
                self.sigStep.emit(self.__rawData, self.__calcData, aveValue, self.__ttype, self.__startTime)
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
                self.__calcData = self.__ttype.getCalcArray(self.__rawData)
                aveValue = np.mean(self.__rawData[:step+1][1], dtype=float)
                aveValue = self.__ttype.getCalcValue(aveValue)
                self.sigStep.emit(self.__rawData[:step+1, :], self.__calcData, aveValue, self.__ttype, self.__startTime)
            self.sigMsg.emit(
                "Worker #{} aborting work at step {}".format(self.__id, totalStep)
            )
            if not control is None:
                GPIO.cleanup()
        self.sigDone.emit(self.__id, self.__ttype)
        return

    # MARK: - Control
    def __controlTemp(self, aveTemp: float, steps: int):
        # TODO: 調整
        if steps <= 0:
            d = self.__presetTemp - aveTemp
            if d <= 1.5:
                return -1
            elif d >= 15:
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
            time.sleep(0.2)
            deltaSeconds = (datetime.datetime.now() - self.__startTime).total_seconds()
            self.__rawData[step] = [deltaSeconds, np.random.normal(), self.__presetTemp]

            if step%9 == 0 and step != 0:
                average = np.mean(self.__rawData[:, 1], dtype=float)
                average = self.__ttype.getCalcValue(average)
                self.__calcData = self.__ttype.getCalcArray(self.__rawData)
                self.sigStep.emit(self.__rawData, self.__calcData, average, self.__ttype, self.__startTime)
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
                aveValue = np.mean(self.__rawData[:step+1][1], dtype=float)
                aveValue = self.__ttype.getCalcValue(aveValue)
                self.__calcData = self.__ttype.getCalcArray(self.__rawData)
                self.sigStep.emit(self.__rawData[:step+1, :], self.__calcData[:step+1, :], aveValue, self.__ttype, self.__startTime)

            self.sigMsg.emit(
                "Worker #{} aborting work at step {}".format(self.__id, totalStep)
            )
        self.sigDone.emit(self.__id, self.__ttype)
        return

if __name__ == "__main__":
    pass