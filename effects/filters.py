def red(image, newval=0):
    image[:,:,2] = newval
    return image

def green(image, newval=0):
    image[:,:,1] = newval
    return image

def blue(image, newval=0):
    image[:,:,0] = newval
    return image