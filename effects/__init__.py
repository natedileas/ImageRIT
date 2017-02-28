from color import red, green, blue
from filters import rotate

key2transforms = {'r': red, 'g': green, 'b': blue}

angle = 0
key2transforms.update(\
    {str(key):lambda frame: rotate(frame, key*360/9.) for key in range(9)})