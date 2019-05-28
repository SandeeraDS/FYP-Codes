import cv2
import time

# input video file
cap = cv2.VideoCapture('../../FYP Videos/3.mp4')
# get frame rate
fps = cap.get(cv2.CAP_PROP_FPS)


# method for text detecting


def detectText(img):


    # 1.Edgedetection(Soble)
    # 2.Dialation(10,1)
    # 3.FindCountors
    # 4.GeaomatricalConstraints

    # Sobel
    sobely = cv2.Sobel(img,cv2.CV_8U, 0, 1, ksize=3)
    retval, threshold = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
    cv2.imshow('frame', threshold)


if not cap.isOpened():
    print('ERROR FILE NOT FOUND OR WRONG CODEC USED!')

while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        time.sleep(1 / fps)  # to run according to frame rate otherwise it go on highSpeed
        # convert BGR to GrayScale
        detectText(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
