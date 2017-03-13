import numpy

"""configuration in the form

f = float, [0, 1]
i = int, [0, 255]
b = binary

config = {
    'r': [f, i, i, b]
    'g': [f, i, i, b]
    'b': [f, i, i, b]
    'k': [f, i, i, b]
}

where in each channel the __ element is:
0th: magnitude
1st: lower bound
2nd: upper bound
3rd: binarization

"""
channels = ['r','g','b','k']

def lut_transforms(image, configuration):

    for i in range(3):
        lut = generate_lut(*configuration[channels[i]])
        image[:,:,i] = lut[image[:,:,i]]
    
    return image

def generate_lut(magnitude, lowerBound, upperBound, binarize=False):
    slope = ((upperBound - lowerBound) / 255.) * magnitude
    lut = numpy.asarray([x * slope for x in range(255)])
    
    if binarize:
        lut = numpy.where(lut > 128, 255, 0)

    return lut
