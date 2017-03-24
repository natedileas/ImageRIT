import sys
    
from PyQt5.QtWidgets import QApplication, QMainWindow

from qt_DisplayWindow import DisplayWindow
from qt_ControlPanel import ControlPanel

def main(camID, config):

    app = QApplication(sys.argv)

    # TODO set up panel window
    control = ControlPanel()
    control.show()

    # set up main display window
    display = DisplayWindow(camID, config, control.get_state)
    display.show()

    

    sys.exit(app.exec_())


if __name__ == '__main__':
    main(0, 'state.json')