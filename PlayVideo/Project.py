import cv2
import time

cap = cv2.VideoCapture('../../FYP Videos/2.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)

if cap.isOpened() == False:
    print('ERROR FILE NOT FOUND OR WRONG CODEC USED!')

while cap.isOpened():
    ret, frame = cap.read()

    if ret == True:
        time.sleep(1 /fps) # to run according to frame rate otherwise it go on highSpeed

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
