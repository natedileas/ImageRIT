
## ImageRIT Viewer:
**Server/qt_main.py:** requires opencv 3.2, python3, pyqt5, numpy, and maybe a few other things I haven't thought of. The server configuration (ip address and port number) need to be changed before running: you can check this on windows with `ipconfig`
  - OpenCV binaries for windows: http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv

## Control App:
**App/ImageRIT_GUI/ImageRIT_GUI.pro:** deploy with qt creator to an android phone or tablet. 
  - Qt Version: 5.8
  - Android Studio Version: 2.3.1
  - ANT Version: 1.10.1
  - API Level: 19-25, dependent on device. Tested on 19 and 25
  - JDK: 8.2.?
  - NDK: ?

### Requirements:
  - **Software:** numpy > 1.12, opencv 3.2, python 3.5, PyQt5
  - **Hardware:** a webcam that be acessed through opencv's VideoCapture Class

### Development History:
Developed on: windows 10 64 bit, x86, dell, python 3.5 (32 Bit), opencv 3.2.0  32 bit

Contact for any questions: ndileas@gmail.com

Credit where credit is due:
  - https://rafaelbarreto.wordpress.com/2011/08/27/a-pyqt-widget-for-opencv-camera-preview/
  - https://www.reddit.com/r/learnpython/comments/34jwlw/showing_opencv_live_video_in_pyqt_gui/
  - https://wiki.qt.io/Qt_for_Android_known_issues
  - http://doc.qt.io/qt-5/androidgs.html
