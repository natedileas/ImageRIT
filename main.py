import Queue
import threading
import multiprocessing

import cv2
import numpy

from effects import effect_functions

class QuitException(Exception): pass

def display(displayQueue, userInputQueue1, userInputQueue2, windowname='window'):
    cv2.namedWindow(windowname)

    state = []

    while 1:
        # consume processed frames
        #userInputQueue1.put(state)
        userInputQueue2.put(state)

        frame = get_item(displayQueue)
        if frame is None:
            continue

        cv2.imshow('Webcam', frame)
        
        key = cv2.waitKey(15)

        if key == -1 or key > 256:
            continue

        key = chr(key)
        if key in ('q', 'Q'):
            print 'quitting'
            break

        elif key in effect_functions.keys():
            state.append(key)


    cv2.destroyAllWindows()
    #userInputQueue1.put('end')
    userInputQueue2.put('end')



def capture(writeQueue, processQueue, messageQueue, source):
    cam = cv2.VideoCapture(source)
    msg = None

    try:
        while True:
            try:
                msg = messageQueue.get(False)
            except Queue.Empty:
                pass

            if msg is 'end': break

            flag, frame = cam.read()
            
            if not flag:
                break

            #writeQueue.put(frame)
            processQueue.put(frame)

    finally:
        cam.release()


def write(writeQueue, userInputQueue, directory, codec='XVID', fps=20.0, \
                                                        out_file='demo.avi'):
    try:
        item = writeQueue.get(True)

        # get an intial frame, then do this
        fourcc = cv2.cv.CV_FOURCC(*codec)
        dims = (item.shape[1], item.shape[0])
        writer = cv2.VideoWriter(directory + '\\' + out_file, fourcc, fps, dims)

        frames_written = 0
        while 1:
            frame = get_item(writeQueue)
            state = get_item(userInputQueue)

            if frame is None or state is None:
                continue

            if state is 'end':
                break

            # write to directory
            writer.write(frame)

    finally:
        writer.release()
        empty_queue(writeQueue)
        empty_queue(userInputQueue)


def get_item(queue, timeout=1):
    item = None
    try:
        item = queue.get(True, timeout)
    except Queue.Empty:
        pass

    return item

def empty_queue(queue):
    while not queue.empty():
        queue.get(False)

def process(processQueue, userInputQueue, displayQueue):
    try:
        while 1:
            frame = get_item(processQueue)
            state = get_item(userInputQueue)

            if frame is None or state is None:
                continue

            if state is 'end':
                break

            # process
            # 1. attachments
            # 2. luts
            # 3. affine / warp

            # send to display
            displayQueue.put(frame)

    finally:
        empty_queue(processQueue)
        empty_queue(userInputQueue)
        empty_queue(displayQueue)

if __name__ == '__main__':
    # initalize queues
    writeQueue = multiprocessing.Queue()
    processQueue = multiprocessing.Queue()
    displayQueue = multiprocessing.Queue()
    input2saveQueue = multiprocessing.Queue()
    input2processQueue = multiprocessing.Queue()
    messageQueue = multiprocessing.Queue()

    # camera
    source = 0
    capture_process = multiprocessing.Process(target=capture, args=(writeQueue, processQueue, messageQueue, source), name='capture_p')
    capture_process.start()

    # video saving
    #directory = '.'
    #writing_thread = multiprocessing.Process(target=write, args=(writeQueue, input2saveQueue, directory), name='writing_p')
    #writing_thread.start()

    # processing
    image_process = multiprocessing.Process(target=process, args=(processQueue, input2processQueue, displayQueue), name='process_p')
    image_process.start()

    # display / user input
    display(displayQueue, input2saveQueue, input2processQueue)
    messageQueue.put('end')
