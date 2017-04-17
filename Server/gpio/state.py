#import pigpio
import threading

def get_state(config, key=0):

    if key == -1 or key > 256:
        return config
    chrkey = chr(key)
    if chrkey in 'Qq':
        print('quitting')
        return

    elif chrkey in 'rgbk':
        # binarize in independent channels
        config['luts'][chrkey][3] = not config['luts'][chrkey][3]

    elif chrkey == "a":
        config['geometric']["affine"]["rotation"] += 5
    elif chrkey == "w":
        config['geometric']["affine"]["scale"] += 0.1
    elif chrkey == "d":
        config['geometric']["affine"]["rotation"] -= 5
    elif chrkey == "s":
        config['geometric']["affine"]["scale"] -= 0.1

    
    # TODO replace with gpio threaded calls

    return config
