import cv2

from . import luts
from . import geometric
from . import filters

from .config import config

def process(frame, state):   
	# frame is array, state is dict containing active funcs
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)[:,::-1]   # flip image --> [::-1]

    for key, val in state.items():
        
        frame = val['func'](frame, *val['args'])

    return frame
