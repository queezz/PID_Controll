"""
https://stackoverflow.com/a/41605909/3730379
"""
import time
import sys
import random

import sys
sys.path.append('..')
TEST = False
try:
    import RPi.GPIO as GPIO
    import AIO
except:
    print('no RPi.GPIO and AIO')
    TEST = True


import time
#import datetime
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import mainwindow
import os
from os.path import join,basename
import numpy as np

from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QPushButton, QTextEdit, QVBoxLayout, QWidget


def trap_exc_during_debug(*args):
    # when app raises uncaught exception, print info
    print(args)


# install exception hook: without this, uncaught exception would cause application to exit
sys.excepthook = trap_exc_during_debug


class Worker(QObject):
    """
    Must derive from QObject in order to emit signals, connect slots to other signals, and operate in a QThread.
    """

    sig_step = pyqtSignal(list)  # worker id, step description: emitted every step through work() loop
    sig_done = pyqtSignal(int)  # worker id: emitted at end of work()
    sig_msg = pyqtSignal(str)  # message to be shown to user
    #passresult = QtCore.pyqtSignal(object) # return data

    def __init__(self, id: int):
        super().__init__()
        self.__id = id
        self.__abort = False
        self.data = []

    @pyqtSlot()
    def work(self):
        """
        Pretend this worker method does work that takes a long time.
        During this time, the thread's event loop is blocked, except if
        the application's processEvents() is called: this gives every
        thread (incl. main) a chance to process events, which in this sample
        means processing signals received from GUI (such as abort).
        """
        thread_name = QThread.currentThread().objectName()
        thread_id = int(QThread.currentThreadId())  # cast to int() is necessary
        self.sig_msg.emit(
            'Running worker #{} from thread "{}" (#{})'.format(
                self.__id, thread_name, thread_id)
        )

        if TEST:
            #for step in range(100):
            step = 0
            while True:
                time.sleep(0.01)
                self.data.append(random.random()*10)
                if step%10 == 0:
                    #self.passresult.emit(np.array(self.data))
                    #self.sig_step.emit((self.__id, self.data))
                    self.sig_step.emit(self.data)
                    self.data = []
                step += 1
                # check if we need to abort the loop; need to process events to receive signals;
                app.processEvents()  # this could cause change to self.__abort
                if self.__abort:
                    # note that "step" value will not necessarily be same for every thread
                    self.sig_msg.emit(
                        'Worker #{} aborting work at step {}'.format(
                            self.__id, step)
                    )
                    break

            self.sig_done.emit(self.__id)
            return

        aio = AIO.AIO_32_0RA_IRC(0x49, 0x3e)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)

        i = 0
        while True:
            voltage = aio.analog_read_volt(0, aio.DataRate.DR_860SPS)

            if True:
                if voltage < 0.7:
                    pass
                    GPIO.output(17,True)
                else:
                    GPIO.output(17,False)

            self.data.append(voltage)
            i += 1

            if i%20 == 0:
                #print(i)
                self.sig_step.emit(self.data)
                self.data = []

            app.processEvents()  # this could cause change to self.__abort
            if self.__abort:
                # note that "step" value will not necessarily be same for every thread
                self.sig_msg.emit(
                    'Worker #{} aborting acquisition'.format(self.__id)
                )
                GPIO.cleanup()
                break

        self.sig_done.emit(self.__id)

    def abort(self):
        self.sig_msg.emit('Worker #{} notified to abort'.format(self.__id))
        self.__abort = True


class MyWidget(QtGui.QMainWindow,mainwindow.Ui_MainWindow):
    NUM_THREADS = 1

    # sig_start = pyqtSignal()  # needed only due to PyCharm debugger bug (!)
    sig_abort_workers = pyqtSignal()

    def __init__(self):
        super(self.__class__,self).__init__()
        self.setupUi(self)

        self.button_start_threads.clicked.connect(self.start_threads)
        self.button_start_threads.setText("Start {} threads".format(self.NUM_THREADS))
        print(self.abort_workers)

        self.button_stop_threads.clicked.connect(self.abort_workers)
        self.button_stop_threads.setText("Stop threads")
        self.button_stop_threads.setDisabled(True)

        # threads can be named, useful for log output
        QThread.currentThread().setObjectName('main')
        self.__workers_done = None
        self.__threads = None

        self.data = []
        self.value_plot = self.p1.plot(pen = '#6ac600')

    def start_threads(self):
        self.log.append('starting {} threads'.format(self.NUM_THREADS))
        self.button_start_threads.setDisabled(True)
        self.button_stop_threads.setEnabled(True)

        self.__workers_done = 0

        # in case that threads did finish work, but did not quit.
        try:
            for thread, worker in self.__threads:
                thread.quit()
                thread.wait()

        except:
            pass

        self.__threads = []
        for idx in range(self.NUM_THREADS):
            worker = Worker(idx)
            thread = QThread()
            thread.setObjectName('thread_' + str(idx))
            # need to store worker too otherwise will be gc'd
            self.__threads.append((thread, worker))
            worker.moveToThread(thread)

            # get progress messages from worker:
            worker.sig_step.connect(self.on_worker_step)
            worker.sig_done.connect(self.on_worker_done)
            worker.sig_msg.connect(self.log.append)

            # control worker:
            self.sig_abort_workers.connect(worker.abort)

            # get read to start worker:
            # self.sig_start.connect(worker.work)  # needed due to PyCharm debugger bug (!); comment out next line
            thread.started.connect(worker.work)
            thread.start()  # this will emit 'started' and start thread's event loop

        # self.sig_start.emit()  # needed due to PyCharm debugger bug (!)

    @pyqtSlot(list)
    def on_worker_step(self, result :list):
        #self.log.append('data update')
        txt = """<font size = 20 color = "#d1451b">{:.2f}</font>""".format(
            result[-1]
        )
        self.value1_bw.setText(txt)
        self.data = np.concatenate((self.data,np.array(result)))
        self.value_plot.setData(
            y = self.data
        )

    @pyqtSlot(int)
    def on_worker_done(self, worker_id):
        self.log.append('worker #{} done'.format(worker_id))
        self.progress.append('-- Signal {} STOPPED'.format(worker_id))
        self.__workers_done += 1
        if self.__workers_done == self.NUM_THREADS:
            self.abort_workers()
            self.log.append('No more workers active')
            self.button_start_threads.setEnabled(True)
            self.button_stop_threads.setDisabled(True)
            # self.__threads = None


    @pyqtSlot()
    def abort_workers(self):
        self.sig_abort_workers.emit()
        self.log.append('Asking each worker to abort')
        # note nice unpacking by Python, avoids indexing
        for thread, worker in self.__threads:
            thread.quit()  # this will quit **as soon as thread event loop unblocks**
            thread.wait()  # <- so you need to wait for it to *actually* quit

        # even though threads have exited, there may still be messages on the main thread's
        # queue (messages that threads emitted before the abort):
        self.log.append('All threads exited')


if __name__ == "__main__":
    app = QApplication([])

    form = MyWidget()
    form.show()

    sys.exit(app.exec_())
