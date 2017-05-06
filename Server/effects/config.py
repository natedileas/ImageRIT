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

    frame_[:, :, 0] = param_lut(rill, riul, numpy.log(rlin) - 2.91, roll, roup)[frame[:, :, 0]]
    frame_[:, :, 1] = param_lut(gill, giul, numpy.log(glin) - 2.91, goll, goup)[frame[:, :, 1]]
    frame_[:, :, 2] = param_lut(bill, biul, numpy.log(blin) - 2.91, boll, boup)[frame[:, :, 2]]
    return frame_.astype(numpy.uint8)


def invert(frame):
    lut = numpy.arange(256, dtype=numpy.uint8)[::-1]
    return lut[frame]


def hsv(frame, h=100, s=100, v=100):
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV).astype(numpy.float64)
    frame_hsv[:, :, 0] *= h / 100
    frame_hsv[:, :, 1] *= s / 100
    frame_hsv[:, :, 2] *= v / 100
    frame_ = cv2.cvtColor(frame_hsv.astype(numpy.uint8), cv2.COLOR_HSV2RGB)
    return frame_


def lab(frame, l=100, a=100, b=100):
    frame_lab = cv2.cvtColor(frame, cv2.COLOR_RGB2Lab).astype(numpy.float64)
    frame_lab[:, :, 0] *= l / 100
    frame_lab[:, :, 1] *= a / 100
    frame_lab[:, :, 2] *= b / 100
    frame_ = cv2.cvtColor(frame_lab.astype(numpy.uint8), cv2.COLOR_Lab2RGB)
    return frame_.astype(numpy.uint8)


def roll_(frame, r, g, b):
    frame[:, :, 0] = numpy.roll(frame[:, :, 0], r)
    frame[:, :, 1] = numpy.roll(frame[:, :, 1], g)
    frame[:, :, 2] = numpy.roll(frame[:, :, 2], b)

    return frame

def flip_h(frame):
    frame_ = numpy.fliplr(frame)
    return frame_

def flip_v(frame):
    frame_ = numpy.flipud(frame)
    return frame_

def quantize(frame, num_colors=256):
    # TODO add log-log scaling
    m = (256 / num_colors) ** 6

    lut = numpy.arange(256, dtype=numpy.uint8)
    lut = lut // m
    lut *= m

    return lut[frame].astype(numpy.uint8)


def perspective(frame, pitch=0, yaw=0):
    # fake perspective transforms
    pass


def circles(frame):
    img = cv2.medianBlur(cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY), 5)

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 40,
                                param1=50, param2=30, minRadius=10, maxRadius=50)

    if circles is None:
        return frame

    circles = numpy.uint16(numpy.around(circles))
    for i in circles[0, :]:
        # draw the outer circle
        cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)

    return frame

def Median(frame, d):
    d = d*2+1
    for band in range(frame.shape[2]):
        frame[:,:,band] = cv2.medianBlur(frame[:,:,band], d)

    return frame

def gaussian(frame, sigma):
    frame_ = cv2.GaussianBlur(frame, (0, 0), sigma)
    return frame_


def oneminusgaussian(frame, sigma):
    frame_ = cv2.Laplacian(frame, cv2.CV_8U, ksize=sigma*2 + 1)
    return frame_

config = {
    "Binarize": {
        "type": "bool-non-momentary",
        "text": "Binarize",
        "func": threshold,
        "args": [127, 255, cv2.THRESH_BINARY]
    },

    "Gamma": {
        "type": "int-dial",
        "text": "Gamma",
        "func": lut,
        "args": [50]
    },

    "affine": {
        "type": "",
        "text": ["Scale", "Rotate"],
        "func": affine,
        "args": [0, 1]
    },

    "color": {
        "func": color,
        "args": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    },

    "invert": {
        "func": invert,
        "args": []
    },
    "hsv": {
        "func": hsv,
        "args": []
    },
    "lab": {
        "func": lab,
        "args": []
    },
    "roll": {
        "func": roll_,
        "args": []
    },
    "flip_h": {
        "func": flip_h,
        "args": []
    },
    "flip_v": {
        "func": flip_v,
        "args": []
    },
    "quantize": {
        "func": quantize,
        "args": []
    },
    "perspective": {
        "func": perspective,
        "args": []
    },
    "circles": {
        "func": circles,
        "args": []
    },
    "Median": {
        "func": Median,
        "args":[]
    }
    "lowpass": {
        "func": gaussian,
        "args": []
    },
    "highpass": {
        "func": oneminusgaussian,
        "args": []
    }
}

# be able to call in process with:
# button = config[id]
# button['func'](frame, *button['params'])