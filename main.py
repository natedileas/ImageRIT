import cv2

from transforms import key2transforms


def transform(frame, keys):
    """ call functions that do the actual processing """ 
    if keys[-1] in '123456789':

    for k in keys:
        if k in key2transforms.keys():
            frame = key2transforms[k](frame)

    return frame


def main(cam, writer, save_video=True):
    cv2.namedWindow('Webcam')
    
    keys = []

    while True:
        flag, frame = cam.read()
        
        if not flag:
            break

        framet = transform(frame, keys)

        cv2.imshow('Webcam', framet)
        
        key = cv2.waitKey(15)

        if save_video:
            writer.write(framet)

        if key == -1 or key > 256:
            continue

        if chr(key) in ('q', 'Q'):
            print 'quitting'
            break

        elif chr(key) in ('c', 'C'):
            print 'clearing'
            keys = []

        elif chr(key) in ('s', 'S'):
            print 'saving'
            # 12 hour, minute
            file_name = time.strftime('screenshots/Imaging@RIT-%I %M.png')
            cv2.imwrite(file_name, framet)

        else:   # the key may correspond to an image transform
            keys.append(chr(key))


if __name__ == '__main__':
    # camera access
    cam = cv2.VideoCapture(0)

    # video saving access
    flag, frame = cam.read()
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    dims = (frame.shape[1], frame.shape[0])
    out = cv2.VideoWriter('demo.avi', fourcc, 20.0, dims)

    main(cam, out)

    cam.release()
    out.release()

    cv2.destroyAllWindows()
