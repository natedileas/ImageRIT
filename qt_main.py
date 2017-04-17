import sys
    
from PyQt5.QtWidgets import QApplication, QMainWindow

from qt_DisplayWindow import DisplayWindow
from imagerit_server import Server

def main(camID):

    hostname = '129.21.52.194'
    port = 12349

    server = Server(hostname, port)
    server.start()

    app = QApplication(sys.argv)

    # set up main display window
    display = DisplayWindow(camID, server.get_state)
    display.show()

    ret = app.exec_()
    server.join()
    sys.exit(ret)


if __name__ == '__main__':
    main(0)
