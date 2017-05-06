import time
import threading
import json

import cv2

from PyQt5 import QtCore
from PyQt5.QtGui import QImage
    
from effects import process

class ImageRIT_PyQt(QtCore.QObject):
    newFrame = QtCore.pyqtSignal(QImage)

    def __init__(self, cameraId, state_func):
        super(ImageRIT_PyQt, self).__init__()
        self.cameraDevice = cv2.VideoCapture(cameraId)
        self.state_func = state_func

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.query_image)
        self._timer.start(1000/30)

    @QtCore.pyqtSlot()
    def query_image(self):
        #time_elapsed = 1 / 30.

        #while 1:
        #    start = time.time()

        # grab frame
        flag, frame = self.cameraDevice.read()
        if not flag: 
            print ('flag')
            return

        # get state
        config = self.state_func()
        #if config is not None: return

        # process
        processed_frame = numpy2qimage(process(frame, config))
        self.newFrame.emit(processed_frame)

        #    while time.time() - start < time_elapsed:
        #        pass

        #self.cameraDevice.release()


def numpy2qimage(array):
    height, width, channel = array.shape
    bytesPerLine = 3 * width
    qImg = QImage(array.copy().data, width, height, bytesPerLine, QImage.Format_RGB888)
    return qImg