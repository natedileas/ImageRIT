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

def affine(frame, rotation, scale):
    rot_deg = 360 - rotation * 3.6 # [0-99] -> [0->356], more to clockwise
    scale = (scale + 1) / 50.
    center = (frame.shape[1] / 2., frame.shape[0] / 2.)
    rot_mat = cv2.getRotationMatrix2D(center, rot_deg, scale)
    frame_ = cv2.warpAffine(frame, rot_mat, (frame.shape[1], frame.shape[0]))

    return frame_

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
    },

    "affine" : {
        "type": "",
        "text": ["Scale", "Rotate"],
        "func": affine,
        "args": [0, 1]
    }
}

# be able to call in process with:
# button = config[id]
# button['func'](frame, *button['params'])