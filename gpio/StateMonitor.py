import json
import time
import threading

import pigpio
import ButtonMonitor

class GPIOStateMonitor(threading.Thread):
    def __init__(self, statequeue, config_file='buttons.json'):
        self.queue = statequeue
        self.config_file = config_file

        with open(self.config_file, 'r') as f:
            self.config = json.load(f)

        self.pi = pigpio.pi()
        self.initialize()

    def initialize(self):
        buttons = []
        for b in self.config['buttons']:
            buttons.append(ButtonMonitor(self.pi, b['pin'], lambda:self.callback_func(b['id'])))

        self.state = dict([(b.id, False) for b in buttons])

    def callback_func(self, button_id):
        self.state[button_id] = not self.state[button_id]

    def run(self):
        interval = 1 / 30.
        sleepinterval = interval / 10.
        start = time.time()

        while 1:
            while time.time() - start < interval:
                time.sleep(sleepinterval)

            statequeue.put(self.state)
