import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QCoreApplication

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "Monitor"
        self.left = 10
        self.top = 10
        # TODO: raspberry pi
        self.width = 640
        self.height = 480

        self.is_start = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.button = QPushButton('start', self)
        # 吹き出し
        self.button.setToolTip('This is an example button')
        # buttonのサイズをいい感じに調整
        self.button.resize(self.button.sizeHint())
        # buttonの位置
        self.button.move(100,70)
        self.button.clicked.connect(lambda: self.on_click(self.is_start))
        # button.clicked.connect(QCoreApplication.instance().quit)

        self.show()

    @pyqtSlot()
    def on_click(self, is_start):
        self.is_start = not self.is_start
        button_title = "stop" if is_start else "start"
        self.button.setText(button_title)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())