import time

import cv2

from effects import process
from gpio.state import get_state


def main(camera, config, max_framerate=1000./30.):
    key = -1

    while True:
        start = time.time()

        # grab frame
        flag, frame = camera.read()
        if not flag: break

        # get state
        state = get_state(config, key)
        if not state: break

        # process
        processed_frame = process(frame, state)

        # display
        cv2.imshow('Webcam', processed_frame)
        key = cv2.waitKey(15)
        flush()

        while time.time() - start < max_framerate:
            pass

def flush():
    while 1:
        if cv2.waitKey(1) == -1:
            break


if __name__ == '__main__':
    import json

    cam = cv2.VideoCapture(0)

    with open('state.json', 'r') as f:
        config = json.load(f)

    #print config
    main(cam, config)

    cam.release()
    cv2.destroyAllWindows()
