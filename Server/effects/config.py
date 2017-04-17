import cv2

threshold = lambda *a: cv2.threshold(*a)[1]

config = {
    "Binarize" : {
        "type": "bool-non-momentary",
        "text": "Binarize",
        "func": threshold,
        "args": [127, 255, cv2.THRESH_BINARY]
    }
}

# be able to call with:
# button = config[id]
# button['func'](frame, *button['params'])