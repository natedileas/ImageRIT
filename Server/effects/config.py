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

def param_lut(in_ll, in_ul, gamma, out_ll, out_ul):
    a = numpy.zeros(256)
    a[in_ll:in_ul] = (numpy.arange(in_ll, in_ul) ** gamma)
    a *= (256 / a.max())
    a[a>=in_ul] = 255

    a = numpy.clip(a, out_ll, out_ul)

    return a.astype(numpy.uint8)

def color(frame, *args):
    """ apply a 3-channel lut transform (also switches b and r channels) """
    frame_ = numpy.zeros(frame.shape)
    rill, riul, rlin, roll, roup, gill, giul, glin, goll, goup, bill, biul, blin, boll, boup = args

    frame_[:,:,0] = param_lut(rill, riul, numpy.log(rlin) - 2.91, roll, roup)[frame[:,:,2]]
    frame_[:,:,1] = param_lut(gill, giul, numpy.log(glin) - 2.91, goll, goup)[frame[:,:,1]]
    frame_[:,:,2] = param_lut(bill, biul, numpy.log(blin) - 2.91, boll, boup)[frame[:,:,0]]
    return frame_.astype(numpy.uint8)


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
    },

    "color" : {
        "func": color,
        "args": [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    }
}

# be able to call in process with:
# button = config[id]
# button['func'](frame, *button['params'])