import cv2
import numpy

threshold = lambda *a: cv2.threshold(*a)[1]

def lut(frame, gamma_in=100, offset=0):
    # gamma_in comes in as [0, 99], maps to [-2, 2]
    # this lets the clipping happen more spectacularly
    gamma = (gamma_in - 50) / 25.

    lut = numpy.arange(256) * gamma
    lut += abs(lut.min())

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