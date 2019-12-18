import time, datetime, math
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
from thermocouple import calcTemperature
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

    sigStep = QtCore.pyqtSignal(np.ndarray, float, ThreadType)
    sigDone = QtCore.pyqtSignal(int, ThreadType)
    sigMsg = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def setWorker(self, id: int, ttype: ThreadType, app: QtGui.QApplication, startTime: datetime, value: int, scale: ScaleSize):
        self.__id = id
        self.__ttype = ttype
        self.__presetTemp = value
        self.__scaleSize = scale
        self.__startTime = startTime
        self.__app = app
        self.__abort = False
        self.__data = np.zeros(shape=(10, 3))

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

    # MARK: - Methodss
    @QtCore.pyqtSlot()
    def work(self):
        self.__setThread()
        if TEST:
            self.__test()
        else:
            if self.__ttype == ThreadType.TEMPERATURE:
                self.__plotTemperature()
            elif self.__ttype == ThreadType.PRESSURE1:
                self.__test()
                pass
            elif self.__ttype == ThreadType.PRESSURE2:
                self.__test()
                pass
            else:
                return

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
        totalStep = 0
        step = 0
        while not (self.__abort):
            time.sleep(0.01)
            deltaSeconds = (datetime.datetime.now() - self.__startTime).total_seconds()
            self.__data[step] = [deltaSeconds, np.random.normal(), self.__presetTemp]

            if step%9 == 0 and step != 0:
                self.sigStep.emit(self.__data, self.__data[-1][1], self.__ttype)
                self.__data = np.zeros(shape=(10, 3))
                step = 0
            else:
                step += 1
            totalStep += 1

            self.__app.processEvents()

        else:
            if self.__data[step][0] == 0.0:
                step -= 1
            if step > -1:
                self.sigStep.emit(self.__data[:step+1, :], self.__data[step, 1], self.__ttype)
            self.sigMsg.emit(
                "Worker #{} aborting work at step {}".format(self.__id, totalStep)
            )
        self.sigDone.emit(self.__id, self.__ttype)
        return

    @QtCore.pyqtSlot()
    def __plotTemperature(self):
        aio = AIO.AIO_32_0RA_IRC(0x49, 0x3e)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)
        totalStep = 0
        step = 0
        aveTemp = 0
        controlStep = -1
        while not (self.__abort):
            time.sleep(0.02)
            voltage = aio.analog_read_volt(0, aio.DataRate.DR_860SPS, pga=5)
            deltaSeconds = (datetime.datetime.now() - self.__startTime).total_seconds()
            temp = calcTemperature(voltage)
            aveTemp += temp
            self.__data[step] = [deltaSeconds, temp, self.__presetTemp]

            if step%9 == 0 and step != 0:
                aveTemp /= 10
                controlStep = self.__control(aveTemp, controlStep)
                self.sigStep.emit(self.__data, aveTemp, self.__ttype)
                self.__data = np.zeros(shape=(10, 3))
                step = 0
            else:
                step += 1
            totalStep += 1

            GPIO.output(17, controlStep > 0)
            controlStep -= 1

            self.__app.processEvents()
        else:
            if self.__data[step][0] == 0.0:
                step -= 1
            if step > -1:
                self.sigStep.emit(self.__data[:step+1, :], self.__data[step, 1], self.__ttype)
            self.sigMsg.emit(
                "Worker #{} aborting work at step {}".format(self.__id, totalStep)
            )
            GPIO.cleanup()
        self.sigDone.emit(self.__id, self.__ttype)
        return

    def __control(self, aveTemp: float, steps: int):
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

if __name__ == "__main__":
    pass
