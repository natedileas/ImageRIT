from . import luts
from . import geometric
from . import filters

from .config import config

def process(frame, state):   
	# frame is array, state is dict containing active funcs

    for key, val in state.items():
        
        frame = val['func'](frame, *val['args'])

    return frame
