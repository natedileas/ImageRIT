import cv2

from .Func import Func 

def rotate(frame, angle=0):
    # frame
    # angle (in degrees)
    rows, cols = frame.shape[0:2]
    
    M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    frame = cv2.warpAffine(frame, M, (cols, rows))

    return frame

effect_functions = {str(key): Func(rotate, key*360/9.) for key in range(9)}