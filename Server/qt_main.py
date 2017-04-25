import sys
import socket

from PyQt5.QtWidgets import QApplication

from qt_DisplayWindow import DisplayWindow
from Server import Server

def main(camID):

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(hostname, ip_address)
    port = 12349

    app = QApplication(sys.argv)

    server = Server('129.21.52.194', port, None)

    # set up main display window
    display = DisplayWindow(camID, server.get_state)
    display.show()

    server.status = display.statusBar
    server.start()

    ret = app.exec_()
    server.join()
    sys.exit(ret)
    


if __name__ == '__main__':
    main(0)
