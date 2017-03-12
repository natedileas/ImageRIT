import threading

import pigpio

class ButtonMonitor(threading.Thread)
    def __init__(self, pi, input_pin, switch_type='NO', timeout=-1):
        self.pi = pi # pigpio open pi object
        self.pin = input_pin   # broadcom
        if not switch_type in ('NO', 'NC'):
            raise ValueError('Switchtype {0} invalid. Options: {1}'.format(switch_type, ('NO', 'NC')))
        self.type = switch_type  # normally on or normally closed
        self.state = False

    def run(self):
        # set up pin
        self.pi.callback(self.pin, pigpio.EITHER_EDGE, self.callback_func)
