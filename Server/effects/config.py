import cv2
import numpy

threshold = lambda *a: cv2.threshold(*a)[1]

def lut(frame, gamma=100, offset=0):
    # valid range for gamma is [-1, 1]
    # comes in as [0, 100]
    gamma /= 50.
    gamma -= 1.
    gamma = 1 - gamma
    gamma = gamma if gamma > -1 else -1
    gamma = gamma if gamma < 1 else 1
    # maps to [-1, 1]
    # checks out -Ryan

    lut = numpy.asarray([x * gamma for x in range(256)])
    lut += lut.min()

    return lut[frame].astype(dtype=numpy.uint8)

config = {
    "Binarize" : {
        "type": "bool-non-momentary",
        "text": "Binarize",
        "func": threshold,
        "args": [127, 255, cv2.THRESH_BINARY]
    },

    "Gamma" : {
        "type": "int-dial",
        "text": "Gamma",
        "func": lut,
        "args": [50]
    }
}

# be able to call in process with:
# button = config[id]
# button['func'](frame, *button['params'])