import time, datetime, math
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui

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

    # test
    def __calcTemperature(self, voltage):
        # V -> μV
        v = voltage * (1e6)

        t = 0.0
        for i in range(2, -3, -1):
            kx = 1
            jx = 10**i
            while(kx>0):
                t += jx
                if t>1372:
                    break
                vta = __calcT(t)
                kx = v-vta
            t -= jx
        return t

    def __calcT(self, tm):
        i = 0
        j = 0
        a = [0]*10
        b = [0]*10
        c = [0]*2
        a[0]= 3.9450128025E01
        a[1]= 2.3622373598E-2
        a[2]=-3.2858906784E-4
        a[3]=-4.9904828777E-6
        a[4]=-6.7509059173E-8
        a[5]=-5.7410327428E-10
        a[6]=-3.1088872894E-12
        a[7]=-1.0451609365E-14
        a[8]=-1.9889266878E-17
        a[9]=-1.6322697486E-20
        b[0]= 3.8921204975E01
        b[1]= 1.8558770032E-02
        b[2]=-9.9457592874E-05
        b[3]= 3.1840945719E-07
        b[4]=-5.6072844889E-10
        b[5]= 5.6075059059E-13
        b[6]=-3.2020720003E-16
        b[7]= 9.7151147152E-20
        b[8]=-1.2104721275E-23
        b[9]=-1.7600413686E01
        c[0]=-1.183432E-04
        c[1]= 1.185976E02

        if tm < -270:
            pass
        elif tm < 0:
            for i in range(1, 11):
                j += a[i-1]*(tm**i)
        elif tm==0:
            j=0
        elif tm <= 1372:
            for i in range(1, 10):
                j += b[i-1]*(tm**i)
            j += b[9]+c[1]*math.exp(c[0]*pow(tm-126.9686,2))
        else:
            pass
        return j

if __name__ == "__main__":
    pass
