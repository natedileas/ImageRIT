import sys
import socket
    
from PyQt5.QtWidgets import QApplication, QMainWindow

from qt_DisplayWindow import DisplayWindow
from Server import Server

def main(camID):

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    port = 12349

    server = Server(ip_address, port)
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
