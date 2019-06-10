import cv2
import time
import numpy as np

# input video file
cap = cv2.VideoCapture('../../../FYP Videos/2.mp4')
# get frame rate
fps = cap.get(cv2.CAP_PROP_FPS)

previous_x = -1
previous_width = -1


def detectText(img,number):
    height, width, channels = img.shape

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_gray = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 3, 18)

    # gradient Magnitude
    sobel_img_x = cv2.Sobel(img_gray, cv2.CV_8U, 1, 0, ksize=3)

    # histogram equalization
    hist_img = cv2.equalizeHist(sobel_img_x)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(10, 2), anchor=(-1, -1))
    img_dilate = cv2.morphologyEx(hist_img, cv2.MORPH_DILATE, kernel, anchor=(-1, -1), iterations=2,
                                  borderType=cv2.BORDER_REFLECT, borderValue=255)
    # Find Contours
    contours, hierarchy = cv2.findContours(img_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # GeaomatricalConstraints
    list = []
    max_width = 0
    max_width_x = 0

    for contour in contours:
        brect = cv2.boundingRect(contour)  # brect = (x,y,w,h)
        ar = brect[2] / brect[3]

        if ar > 2 and brect[2] > 40 and brect[3] > 20 and brect[3] < 100:
            list.append(brect)
            if (max_width < brect[2]):
                max_width = brect[2]
                max_width_x = brect[0]

    for r in list:
        # draw region of interest
        cv2.rectangle(img, (r[0], r[1]), (r[0] + r[2], r[1] + r[3]), (250, 0, 0), 2)

    # global previous_x
    # global previous_width
    # if max_width_x != previous_x and max_width != previous_width and max_width > 200:
    #     cv2.imwrite("image/"+str(count)+".jpg", img)
    #     previous_x = max_width_x
    #     previous_width = max_width

    cv2.imshow("Original", img)
    cv2.imshow("Threshhold", img_gray)


if not cap.isOpened():
    print('ERROR FILE NOT FOUND OR WRONG CODEC USED!')
count =1
while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        time.sleep(1 / fps)  # to run according to frame rate otherwise it go on highSpeed
        # convert BGR to GrayScale
        detectText(frame,count)
        count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
