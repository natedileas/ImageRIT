import cv2

def affine_transforms(frame, config):
    """
    args:
        frame: image (numpy array)
        angle: rotation angle (in degrees)
        scale: scale factor (scalar)
    """
    angle = config["rotation"]
    scale = config["scale"]

    rows, cols = frame.shape[0:2]
    
    M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, scale)
    frame = cv2.warpAffine(frame, M, (cols, rows), flags=cv2.INTER_AREA)

    return frame

