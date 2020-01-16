import time, pigpio
from pyqtgraph.Qt import QtCore
from customTypes import ThreadType

# must inherit QtCore.QObject in order to use 'connect'
class ElectricCurrent(QtCore.QObject):
    def __init__(self, pi):
        super().__init__()
        self.pi = pi
        # range 0~0.01
        self.__onLight = 0
        self.abort = False

    # MARK: setter
    def setOnLight(self, value: float):
        self.__onLight = value

    # MARK: - Methods
    @QtCore.pyqtSlot()
    def work(self):
        self.__setThread()
        pinNum = ThreadType.getGPIO(ThreadType.TEMPERATURE)
        self.pi.set_mode(pinNum, pigpio.OUTPUT)
        while not self.abort:
            self.pi.write(pinNum, 1)
            time.sleep(self.__onLight)
            self.pi.write(pinNum, 0)
            time.sleep(0.01-self.__onLight)
        else:
            self.pi.stop()

    def __setThread(self):
        threadName = QtCore.QThread.currentThread().objectName()
        threadId = int(QtCore.QThread.currentThreadId())
    
    @QtCore.pyqtSlot()
    def setAbort(self):
        self.abort = True

if __name__ == "__main__":
    pass