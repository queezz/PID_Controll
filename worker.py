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

            # TODO: measure data and calculate
            self.__data[step] = [deltaSeconds, voltage]

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

if __name__ == "__main__":
    pass
