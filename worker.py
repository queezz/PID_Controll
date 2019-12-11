import time
import datetime
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

TEST = False
try:
    import RPi.GPIO as GPIO
    import AIO
except:
    print("no RPi.GPIO or AIO")
    TEST = True

# must inherit QtCore.QObject in order to use 'connect'
class Worker(QtCore.QObject):

    sigStep = QtCore.pyqtSignal(str, np.ndarray)
    sigDone = QtCore.pyqtSignal(int, str)
    sigMsg = QtCore.pyqtSignal(str)

    def __init__(self, id: int, type: str, app: QtGui.QApplication, value: int):
        super().__init__()
        self.__id = id
        self.__type = type
        self.__temperature = value
        self.__app = app
        self.__abort = False
        self.__data = np.zeros(shape=(10, 2))

    @QtCore.pyqtSlot()
    def work(self):
        self.__setThread()
        if TEST:
            self.__test()
        else:
            if self.__type == "Temperature":
                self.__plotTemperature()
            elif self.__type == "Pressure1":
                self.__test()
                pass
            elif self.__type == "Pressure2":
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
        startTime = datetime.datetime.now()
        totalStep = 0
        step = 0
        while not (self.__abort):
            time.sleep(0.01)
            currentTime = datetime.datetime.now()
            deltaSeconds = (currentTime - startTime).total_seconds()

            self.__data[step] = [deltaSeconds, np.random.normal()]

            if step%9 == 0 and step!=0:
                self.sigStep.emit(self.__type, self.__data)
                self.__data = np.zeros(shape=(10, 2))
                step = 0
            else:
                step += 1
            totalStep += 1

            self.__app.processEvents()

        else:
            if self.__data[step][0] == 0.0:
                step -= 1
            if step > -1:
                self.sigStep.emit(self.__type, self.__data[:step+1, :])
            self.sigMsg.emit(
                "Worker #{} aborting work at step {}".format(self.__id, totalStep)
            )
        self.sigDone.emit(self.__id, self.__type)
        return

    @QtCore.pyqtSlot()
    def __plotTemperature(self):
        print(self.__temperature)
        aio = AIO.AIO_32_0RA_IRC(0x49, 0x3e)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)
        startTime = datetime.datetime.now()
        totalStep = 0
        step = 0
        while not (self.__abort):
            time.sleep(0.01)
            voltage = aio.analog_read_volt(0, aio.DataRate.DR_860SPS)
            currentTime = datetime.datetime.now()
            deltaSeconds = (currentTime - startTime).total_seconds()
            temp = self.__calcTemperature(voltage)

            # TODO: measure data and calculate
            self.__data[step] = [deltaSeconds, temp]

            # TODO: PID Controll
            self.__PIDControll(voltage)

            if step%9 == 0 and step!=0:
                self.sigStep.emit(self.__type, self.__data)
                self.__data = np.zeros(shape=(10, 2))
                step = 0
            else:
                step += 1
            totalStep += 1

            self.__app.processEvents()

        else:
            if self.__data[step][0] == 0.0:
                step -= 1
            if step > -1:
                self.sigStep.emit(self.__type, self.__data[:step+1, :])
            self.sigMsg.emit(
                "Worker #{} aborting work at step {}".format(self.__id, totalStep)
            )
            GPIO.cleanup()
        self.sigDone.emit(self.__id, self.__type)
        return

    def __PIDControll(self, voltage):
        # TODO: TEST
        if voltage < 3.3:
            GPIO.output(17, True)
        else:
            GPIO.output(17, False)

    def __calcTemperature(self, voltage):   # type K: 試し
        c1 = 2.508355 * (1e-2)
        c2 = 7.860106 * (1e-8)
        c3 = -2.503131 * (1e-10)
        c4 = 8.315270 * (1e-14)
        c5 = -1.228034 * (1e-17)
        c6 = 9.804036 * (1e-22)
        c7 = -4.413030 * (1e-26)
        c8 = 1.057734 * (1e-30)
        c9 = -1.052755 * (1e-35)

        t = c1 * t + c2 * pow(t, 2) + c3*pow(t, 3) + c4*pow(t, 4) + c5*pow(t, 5) + c6*pow(t, 6) + c7*pow(t, 7) + 83*pow(t, 8) + c9*pow(t, 9)

        return t

if __name__ == "__main__":
    pass
