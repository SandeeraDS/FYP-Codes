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

    # linear contrast stretching
    minmax_img = cv2.normalize(img, 0, 255, norm_type=cv2.NORM_MINMAX)

    # histogram equalization
    # hist_img = cv2.equalizeHist(minmax_img)

    # 1.Edge detection(Sobel)
    # 2.Dilation(10,1)
    # 3.Find Contours
    # 4.GeometricalConstraints

    # Sobel
    sobel_img_x = cv2.Sobel(minmax_img, cv2.CV_8U, 1, 0, ksize=3)
    # sobel_img_y = cv2.Sobel(minmax_img, cv2.CV_8U, 0, 1, ksize=3)

    # blened_img = cv2.addWeighted(src1=sobel_img_x, alpha=0.5, src2=sobel_img_y, beta=0.5, gamma=0)

    retval, threshold = cv2.threshold(sobel_img_x, 244, 255, cv2.THRESH_BINARY)

    # Dilation
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(10, 2), anchor=(-1, -1))
    img_dilate = cv2.morphologyEx(threshold, cv2.MORPH_DILATE, kernel, anchor=(-1, -1), iterations=2,
                                  borderType=cv2.BORDER_REFLECT, borderValue=255)

    # Find Contours
    contours, hierarchy = cv2.findContours(img_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # GeaomatricalConstraints
    list = []
    for i in range(len(contours)):
        brect = cv2.boundingRect(contours[i])  # brect = (x,y,w,h)
        ar = brect[2] / brect[3]

        if ar > 2 and brect[2] > 40 and brect[3] > 16 and brect[3] < 100:
            list.append(brect)
            cv2.drawContours(image, contours, i, (0, 255, 0), 2)

    # for r in list:
    #     cv2.rectangle(image, (r[0], r[1]), (r[0] + r[2], r[1] + r[3]), (250, 0, 0), 2)

    cv2.imshow('frame', image)
    # cv2.imshow('frame2', img_dilate)


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
