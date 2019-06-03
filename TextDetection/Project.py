import cv2
import time
import numpy as np

# input video file
cap = cv2.VideoCapture('../../FYP Videos/2.mp4')
# get frame rate
fps = cap.get(cv2.CAP_PROP_FPS)


# method for text detecting


def detectText(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 1.Edgedetection(Soble)
    # 2.Dialation(10,1)
    # 3.FindCountors
    # 4.GeaomatricalConstraints

    # Sobel
    sobely = cv2.Sobel(img, cv2.CV_8U, 0, 1, ksize=3)

    retval, threshold = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)

    # Dialtion
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(10, 1), anchor=(-1, -1))
    img_dilate = cv2.morphologyEx(threshold, cv2.MORPH_DILATE, kernel, anchor=(-1, -1), iterations=1,
                                  borderType=cv2.BORDER_REFLECT, borderValue=255)



    #find Contours
    contours, hierarchy = cv2.findContours(img_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # GeaomatricalConstraints
    List = []
    for contour in contours:
        brect = cv2.boundingRect(contour)
        ar = brect[2] / brect[3]

        if brect[2] > 30 and brect[3] > 8 and brect[3] < 100:
            List.append(brect)

    for r in List:
        cv2.rectangle(image, (r[0], r[1]), (r[0] + r[2], r[1] + r[3]), (250, 0, 0), 2)





    cv2.imshow('frame',image)


if not cap.isOpened():
    print('ERROR FILE NOT FOUND OR WRONG CODEC USED!')

while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        time.sleep(1 / fps)  # to run according to frame rate otherwise it go on highSpeed
        # convert BGR to GrayScale
        detectText(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
