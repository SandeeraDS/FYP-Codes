import cv2
import time
import numpy as np

# input video file
cap = cv2.VideoCapture('../../../FYP Videos/222.mp4')
# get frame rate
fps = cap.get(cv2.CAP_PROP_FPS)

previous_image = None
firstFrame = False


# method for text detecting


def detectText(image, number):
    height, width, channels = image.shape
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # linear contrast stretching
    minmax_img = cv2.normalize(img, 0, 255, norm_type=cv2.NORM_MINMAX)

    # Sobel
    sobel_img_x = cv2.Sobel(minmax_img, cv2.CV_8U, 1, 0, ksize=3)

    retval, threshold = cv2.threshold(sobel_img_x, 244, 255, cv2.THRESH_BINARY)

    # Dilation
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(10, 2), anchor=(-1, -1))
    img_dilate = cv2.morphologyEx(threshold, cv2.MORPH_DILATE, kernel, anchor=(-1, -1), iterations=2,
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

    global previous_image
    global firstFrame

    if max_width > 200:

        if not firstFrame:
            firstFrame = True
            # crop_img = threshold[0:height, max_width_x:max_width_x + max_width]
            crop_img = img[0:height, max_width_x:max_width_x + max_width]

            previous_image = crop_img
            cv2.imwrite("image/" + str(count) + ".jpg", crop_img)
        else:
            crop_img = img[0:height, max_width_x:max_width_x + max_width]

            if previous_image.shape == crop_img.shape:
                different = cv2.subtract(src1=previous_image, src2=crop_img)
                if cv2.countNonZero(different) != 0:
                    cv2.imwrite("image/" + str(count) + ".jpg", crop_img)
                    previous_image = crop_img
                    print("pixel Changed")
                    cv2.imshow('frame', crop_img)
            else:
                cv2.imwrite("image/" + str(count) + ".jpg", crop_img)
                print("size Changed")
                previous_image = crop_img
                cv2.imshow('frame', crop_img)

    # for r in list:
    #     # draw region of interest
    #     cv2.rectangle(image, (r[0], r[1]), (r[0] + r[2], r[1] + r[3]), (250, 0, 0), 2)

    # cv2.imshow('frame', image)
    # cv2.imshow('frame2', img_dilate)


if not cap.isOpened():
    print('ERROR FILE NOT FOUND OR WRONG CODEC USED!')
count = 1
while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        # time.sleep(1 / fps)  # to run according to frame rate otherwise it go on highSpeed
        # convert BGR to GrayScale
        detectText(frame, count)
        count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
