import time
import threading
import json

import cv2

from PyQt5 import QtCore
from PyQt5.QtGui import QImage
    
from effects import process
from gpio.state import get_state  # To be replaced with an appropriate qt call

class ImageRIT_PyQt(QtCore.QObject):
    newFrame = QtCore.pyqtSignal(QImage)

    def __init__(self, cameraId=0, config_file='state.json'):
        super(ImageRIT_PyQt, self).__init__()
        self.cameraDevice = cv2.VideoCapture(cameraId)

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.query_image)
        self._timer.start(1000/30)

        with open(config_file, 'r') as f:
            self.config = json.load(f)
    
    @QtCore.pyqtSlot()
    def query_image(self):
        #time_elapsed = 1 / 30.
        #tate = self.config

        #while 1:
        #    start = time.time()

        # grab frame
        flag, frame = self.cameraDevice.read()
        if not flag: return

        # get state
        self.config = get_state(self.config, -1)
        if not self.config: return

        # process
        processed_frame = numpy2qimage(process(frame, self.config))

        self.newFrame.emit(processed_frame)

        #    while time.time() - start < time_elapsed:
        #        pass

        #self.cameraDevice.release()


def numpy2qimage(array):
    height, width, channel = array.shape
    bytesPerLine = 3 * width
    qImg = QImage(array.data, width, height, bytesPerLine, QImage.Format_RGB888)
    return qImg