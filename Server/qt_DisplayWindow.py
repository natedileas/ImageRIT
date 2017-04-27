from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import PyQt5.QtGui

import time
import os
import threading

from qt_CameraWidget import ImageRIT_PyQt
from g_api_email import send_async


class DisplayWindow(QMainWindow):
    save_name = os.getcwd() + '\\output\\TEMP.png'

    def __init__(self, cameraId, state_func):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.cam = ImageRIT_PyQt(cameraId, state_func)
        self.cam.newFrame.connect(self.display)

        self.setWindowIcon(PyQt5.QtGui.QIcon('..\logo_120x120.png'))
        self.setWindowTitle('ImageRIT')

        # selfie / email variable
        self._image_name = None
    
    def mouseDoubleClickEvent(self, mouseevent):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    @QtCore.pyqtSlot(QImage)
    def display(self, frame):
        self.ui.ImageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.ImageLabel.setPixmap(QPixmap.fromImage(frame).scaled( \
            self.ui.ImageLabel.size(), QtCore.Qt.KeepAspectRatio, \
            QtCore.Qt.FastTransformation))
        self.ui.ImageLabel.update()

    @QtCore.pyqtSlot(str)
    def show_msg(self, msg):
        if 'Connected:' in msg:
            msg += '|'+self.ui.statusBar.text()
        elif 'Disconnected:' in msg:
            # remove connected statement from status
            curr = self.ui,statusBar.text().split('|')
            new = []
            for section in curr:
                if msg[-5:] in section:
                    new.append(msg)
                else:
                    new.append(section)
            msg = new
        self.ui.statusBar.showMessage(msg)

    @QtCore.pyqtSlot(dict)
    def selfie(self, data):
        self._image_name = self.save_name.format(int(round(time.time())))
        self.ui.ImageLabel.pixmap().save(self._image_name, "PNG")
    
    @QtCore.pyqtSlot(dict)
    def email(self, data):
        email = data['email']
        if self._image_name:
            threading.Thread(target=lambda:send_async(email, self._image_name)).start()
        self._image_name = None

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 601)
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
        MainWindow.setCentralWidget(self.VideoStream)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setStyleSheet("border-top-color: rgb(0, 0, 0);\n"
            "background-color: rgb(0, 0, 0);\n"
            "color: rgb(255, 255, 255);")
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

