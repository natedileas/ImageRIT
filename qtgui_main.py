import time
import json
import threading

import cv2
import numpy
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtGui
from PyQt5.QtGui import QImage, QPixmap
    
from effects import process
from gpio.state import get_state

class CameraWidget(QtCore.QObject):

    _DEFAULT_FPS = 30.

    newFrame = QtCore.pyqtSignal(numpy.ndarray)

    def __init__(self, cameraId, ui, config, parent=None):
        super(CameraWidget, self).__init__(parent)

        self.ui = ui
        self.config = config
        self.newFrame.connect(self.display)

        self._cameraDevice = cv2.VideoCapture(cameraId)
        self.stop = False

        t = threading.Thread(target=self.run)
        t.start()
        

    def run(self):
        max_framerate= 1./30.
        state = self.config

        while not self.stop:
            start = time.time()

            # grab frame
            flag, frame = self._cameraDevice.read()
            if not flag: break

            # get state
            state = get_state(state, -1)
            if not state: break

            # process
            processed_frame = process(frame, state)

            self.newFrame.emit(processed_frame)

            while time.time() - start < max_framerate:
                pass

        self._cameraDevice.release()


    @QtCore.pyqtSlot(numpy.ndarray)
    def display(self, frame):
        img = numpy2qimage(frame)
        self.ui.ImageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.ImageLabel.setPixmap(QPixmap.fromImage(img).scaled(self.ui.ImageLabel.size(), \
            QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation))
        self.ui.ImageLabel.update()

    @property
    def frameSize(self):
        w = self._cameraDevice.get(3)
        h = self._cameraDevice.get(4)
        return int(w), int(h)


def numpy2qimage(array):
    height, width, channel = array.shape
    bytesPerLine = 3 * width
    qImg = QImage(array.data, width, height, bytesPerLine, QImage.Format_RGB888)
    return qImg


@QtCore.pyqtSlot(numpy.ndarray)
def process_frame(frame):
    p_frame = process(frame)


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(243, 110, 33);")
        self.VideoStream = QtWidgets.QWidget(MainWindow)
        self.VideoStream.setObjectName("VideoStream")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.VideoStream)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ImageLabel = QtWidgets.QLabel(self.VideoStream)
        self.ImageLabel.setText("")
        self.ImageLabel.setObjectName("ImageLabel")
        self.verticalLayout.addWidget(self.ImageLabel)
        self.selfie = QtWidgets.QPushButton(self.VideoStream)
        self.selfie.setObjectName("selfie")
        self.verticalLayout.addWidget(self.selfie)
        MainWindow.setCentralWidget(self.VideoStream)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.selfie.setText(_translate("MainWindow", "SELFIE"))

def main():

    with open('state.json', 'r') as f:
        config = json.load(f)

    app = QApplication(sys.argv)
    main = QMainWindow()
    
    ui = Ui_MainWindow()
    ui.setupUi(main)
    main.show()

    cam = CameraWidget(0, ui, config)

    sys.exit(app.exec_())


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow

    main()