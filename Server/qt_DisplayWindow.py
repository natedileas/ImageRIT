from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import PyQt5.QtGui

from qt_CameraWidget import ImageRIT_PyQt


class DisplayWindow(QMainWindow):
    def __init__(self, cameraId, state_func):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.cam = ImageRIT_PyQt(cameraId, state_func)
        self.cam.newFrame.connect(self.display)

        self.setWindowIcon(PyQt5.QtGui.QIcon('..\logo_120x120.png'))
        self.setWindowTitle('ImageRIT')
    
    def mouseDoubleClickEvent(self, mouseevent):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    @QtCore.pyqtSlot(QImage)
    def display(self, frame):
        self.ui.ImageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.ImageLabel.setPixmap(QPixmap.fromImage(frame).scaled(self.ui.ImageLabel.size(), \
            QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation))
        self.ui.ImageLabel.update()

    @QtCore.pyqtSlot(str)
    def show_msg(self, msg):
        self.ui.statusBar.showMessage(msg)


    @QtCore.pyqtSlot(str)
    def selfie(self, time):
        #delta = time - current  # TODO use timestamp
        QtCore.QTimer.singleShot(3000, self.save)

    @QtCore.pyqtSlot(str)
    def email(self, email):
        print ('email')

    @QtCore.pyqtSlot()
    def save(self):
        # save this image
        p = self.ui.ImageLabel.pixmap().save("C:\\Users\\Natethegreat\\Code\\filename.jpg", "JPG")

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

