import cv2

def apply_geometric(frame, config):
    affine_frame = affine_transforms(frame, config["affine"])
    warp_frame = warp(affine_frame, config["warp"])

    return warp_frame

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


def warp(frame, config):
    return frame
