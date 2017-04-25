import sys
import socket

from PyQt5.QtWidgets import QApplication

from qt_DisplayWindow import DisplayWindow
from Server import Server

def main(camID):

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname_ex(hostname)[2][-1]
    print(hostname, ip_address)
    port = 12349

    app = QApplication(sys.argv)

    server = Server(ip_address, port)

    # set up main display window
    display = DisplayWindow(camID, server.get_state)
    display.show()

    server.status.connect(display.show_msg)
    server.start()

    ret = app.exec_()
    server.join()
    sys.exit(ret)

if __name__ == '__main__':
    main(0)
