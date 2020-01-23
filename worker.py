import time, datetime
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
from typing import Callable
from customTypes import ThreadType
from electricCurrent import ElectricCurrent

TEST = False

# Specify cable connections to ADC
CHP1 = 15
CHP2 = 16
CHT  = 1

# Raspi outputs


TIMESLEEP = 0.015
# Number of data points for collection, steps%STEP == 0
STEP = 5

try:
    from AIO import AIO_32_0RA_IRC as adc
    import pigpio
except:
    print("no pigpio or AIO")
    TEST = True

# must inherit QtCore.QObject in order to use 'connect'
class Worker(QtCore.QObject):

    sigStep = QtCore.pyqtSignal(np.ndarray, np.ndarray, float, ThreadType, datetime.datetime)
    sigDone = QtCore.pyqtSignal(int, ThreadType)
    sigMsg = QtCore.pyqtSignal(str)

    sigAbortHeater = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

    def setWorker(self, id: int, ttype: ThreadType, app: QtGui.QApplication,
                  startTime: datetime.datetime, value: int,**kws):
        self.__id = id
        self.__ttype = ttype
        self.__app = app
        self.__abort = False
        self.__startTime = startTime
        self.__presetTemp = value
        self.__rawData = np.zeros(shape=(STEP, 3))
        self.__calcData = np.zeros(shape=(STEP, 3))
        self.__IGmode = kws.get('IGmode','Torr')
        self.__IGrange= kws.get('IGrange',-3)

        if not TEST:
            self.pi = pigpio.pi()
            self.__onLight= 0.1
            self.__sumE = 0
            self.__exE = 0

    # MARK: - Getters
    def getThreadType(self):
        return self.__ttype

    def getStartTime(self):
        return self.__startTime

    # MARK: - Setters
    def setPresetTemp(self, newTemp: int):
        self.__presetTemp = newTemp
        return

    def setIGmode(self, IGmode):
        self.__IGmode = IGmode
        print(self.__IGmode)
        return

    def setIGrange(self, IGrange):
        self.__IGrange= IGrange
        print(10**self.__IGrange)
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
    def __plotPlasma(self):
        # TODO: pinId, control
        self.__plot(3, 4)

    def __plotTemp(self):
        self.__plotT()

    def __plotPress1(self):
        self.__plot(CHP1, adc.PGA.PGA_10_0352V)

    def __plotPress2(self):
        self.__plot(CHP2, adc.PGA.PGA_10_0352V)

    def __plot(self, pId: int, fscale: int):
        """ control - a method to control Temperature (or other)
        control = self.__controlTemp for temperature control
        """
        
        aio = adc(0x49, 0x3e) # instance of AIO_32_0RA_IRC from AIO.py
        # Why this addresses?
        
        totalStep = 0
        step = 0
        
        while not (self.__abort):
            time.sleep(TIMESLEEP)
            
            # READ DATA
            voltage = aio.analog_read_volt(pId, aio.DataRate.DR_860SPS, pga=fscale)

            deltaSeconds = (datetime.datetime.now() - self.__startTime).total_seconds()
            if self.__ttype == ThreadType.PRESSURE1:
                m = 10**self.__IGrange
                print(m)
            else:
                m = 1
            value = self.__ttype.getCalcValue(voltage,IGrange=m)

            # READ DATA
            #  I do not know why this is needed
            #  What happens if these two lines are removed?
            #  Just reading from two channels, right? Some communication problem?
            aio.analog_read_volt(CHP1, aio.DataRate.DR_860SPS, pga=2)
            aio.analog_read_volt(CHP2, aio.DataRate.DR_860SPS, pga=2)

            self.__rawData[step] = [deltaSeconds, voltage, self.__presetTemp]

            if step%(STEP-1) == 0 and step != 0:
                # average 10 points of data
                aveValue = np.mean(self.__rawData[:, 1], dtype=float)
                # convert vlots to actual value
                aveValue = self.__ttype.getCalcValue(aveValue)
                    
                self.__calcData = self.__ttype.getCalcArray(self.__rawData)
                self.sigStep.emit(self.__rawData, self.__calcData, aveValue, self.__ttype, self.__startTime)
                self.__rawData = np.zeros(shape=(STEP, 3))
                self.__calcData = np.zeros(shape=(STEP, 3))
                step = 0
            else:
                step += 1
            totalStep += 1                
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

        self.sigDone.emit(self.__id, self.__ttype)
        return

    # temperature plot
    @QtCore.pyqtSlot()
    def __plotT(self):
        sensor = self.pi.spi_open(CHT, 1000000, 0)

        eCurrent = ElectricCurrent(self.pi, self.__app)
        thread = QtCore.QThread()
        thread.setObjectName("heater current")
        eCurrent.moveToThread(thread)
        thread.started.connect(eCurrent.work)
        self.sigAbortHeater.connect(eCurrent.setAbort)
        thread.start()

        totalStep = 0
        step = 0

        while not (self.__abort):
            time.sleep(0.25)
            temp = -1000

            # READ DATA
            c, d = self.pi.spi_read(sensor, 2) # if c==2: ok else: ng
            if c == 2:
                word = (d[0]<<8) | d[1]
                if (word & 0x8006) == 0: # Bits 15, 2, and 1 should be zero.
                    temp = (word >> 3)/4.0
                else:
                    print("bad reading {:b}".format(word))

            deltaSeconds = (datetime.datetime.now() - self.__startTime).total_seconds()
            self.__rawData[step] = [deltaSeconds, temp, self.__presetTemp]

            if step%(STEP-1) == 0 and step != 0:
                # average 10 points of data
                aveValue = np.mean(self.__rawData[:, 1], dtype=float)

                # CONTROL
                self.__controlTemp(aveValue, eCurrent)
                
                self.sigStep.emit(self.__rawData, self.__rawData, aveValue, self.__ttype, self.__startTime)
                self.__rawData = np.zeros(shape=(STEP, 3))
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
                self.sigStep.emit(self.__rawData[:step+1, :], self.__rawData[:step+1, :], aveValue, self.__ttype, self.__startTime)
            self.sigMsg.emit(
                "Worker #{} aborting work at step {}".format(self.__id, totalStep)
            )
            self.sigAbortHeater.emit()
            self.__sumE = 0
            thread.quit()
            thread.wait()
            self.pi.spi_close(sensor)
            self.pi.stop()

        self.sigDone.emit(self.__id, self.__ttype)

    # MARK: - Control
    def __controlTemp(self, aveTemp: float, eCurrent: ElectricCurrent):
        e = self.__presetTemp - aveTemp
        integral = self.__sumE + e * TIMESLEEP
        derivative = (e - self.__exE) / TIMESLEEP

        # TODO: 調整
        Kp = 3.5
        Ki = 0.06
        Kd = 0

        # TODO: self._onLight を変更する
        if e >= 0:
            output = Kp * e + Ki * integral + Kd * derivative
            output = output * 0.0002 


            print(output)
            eCurrent.setOnLight(max(output, 0))
        else:
            eCurrent.setOnLight(0)
        self.__exE = e
        self.__sumE = integral

    # MARK: - Test
    def __test(self):
        totalStep = 0
        step = 0
        while not (self.__abort):
            #print(self.__ttype)
            if self.__ttype == ThreadType.PLASMA:
                val = (np.random.normal()+2.5)
                time.sleep(TIMESLEEP)
                STEPtest = STEP
            elif self.__ttype == ThreadType.TEMPERATURE:
                val = (np.random.normal()+1)/10000
                time.sleep(0.25)
                STEPtest = 2 
            elif self.__ttype == ThreadType.PRESSURE1:
                val = (np.random.normal()+1)*5
                time.sleep(TIMESLEEP)
                STEPtest = STEP
            elif self.__ttype == ThreadType.PRESSURE2:
                val = (np.random.normal()+1)*5
                time.sleep(TIMESLEEP)
                STEPtest = STEP
            else:
                return
            deltaSeconds = (datetime.datetime.now() - self.__startTime).total_seconds()
            self.__rawData[step] = [deltaSeconds, val, self.__presetTemp]
            if self.__ttype == ThreadType.PRESSURE1:
                m = 10**self.__IGrange
            else:
                m = 1

            if step%(STEPtest-1) == 0 and step != 0:
                average = np.mean(self.__rawData[:, 1], dtype=float)
                average = self.__ttype.getCalcValue(average,IGrange=m)
                self.__calcData = self.__ttype.getCalcArray(self.__rawData,IGrange=m)
                self.sigStep.emit(self.__rawData, self.__calcData, average, self.__ttype, self.__startTime)
                self.__rawData = np.zeros(shape=(STEPtest, 3))
                self.__calcData = np.zeros(shape=(STEPtest, 3))
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
                aveValue = self.__ttype.getCalcValue(aveValue,IGrange=m)
                self.__calcData = self.__ttype.getCalcArray(self.__rawData,IGrange=m)
                self.sigStep.emit(self.__rawData[:step+1, :], self.__calcData[:step+1, :], aveValue, self.__ttype, self.__startTime)

            self.sigMsg.emit(
                "Worker #{} aborting work at step {}".format(self.__id, totalStep)
            )
        self.sigDone.emit(self.__id, self.__ttype)
        return

if __name__ == "__main__":
    pass
