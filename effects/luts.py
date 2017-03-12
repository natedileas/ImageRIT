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
channels = ['r', 'g', 'b', 'k']

def lut_transforms(image, configuration):

    lut = numpy.zeros((255,3))

    for i in range(3):
        lut[:,:,i] = generate_lut(*configuration[channels[i]])
        image[:,:,i] = lut[:,:,i][image[:,:,i]]
    
    lut = numpy.where(lut > 255, 255 - lut, lut)

    return lut[image]

def generate_lut(magnitude, lowerBound, upperBound, binarize=False):
    lut = numpy.asarray([x * (upperBound - lowerBound) * magnitude for x in range(255)])
    
    if binarize == True:
        lut = numpy.where(lut > 128, 255, 0)

    return lut
