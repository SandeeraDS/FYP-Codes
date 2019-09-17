import cv2
import time
import numpy as np

# input video file
cap = cv2.VideoCapture('../../../FYP Videos/114.mp4')
# get frame rate
fps = cap.get(cv2.CAP_PROP_FPS)


# method for text detecting


def detectText(image, i):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height,weight = img.shape
    # linear contrast stretching
    minmax_img = cv2.normalize(img, 0, 255, norm_type=cv2.NORM_MINMAX)

    img_empty = np.zeros([height, weight], dtype=np.uint8)
    img_empty.fill(255)
    #img_Blurred = cv2.GaussianBlur(minmax_img, (3, 3), 0)

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
    im2,contours, hierarchy = cv2.findContours(img_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # GeaomatricalConstraints
    list = []
    for contour in contours:
        brect = cv2.boundingRect(contour)  # brect = (x,y,w,h)
        ar = brect[2] / brect[3]

        if ar > 2.2 and brect[2] > 40 and brect[3] > 15 and brect[3] < 100:
            list.append(brect)

    for r in list:
        # draw region of interest
        cv2.rectangle(image, (r[0], r[1]), (r[0] + r[2], r[1] + r[3]), (250, 0, 0), 2)
        #retval, threshold = cv2.threshold(img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]], 125, 255, cv2.THRESH_BINARY)
        #img22 = cv2.medianBlur(img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]], 3)
        blur = cv2.GaussianBlur(img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]], (3, 3), 0)
        threshold = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 7)
        kernel = np.ones((1, 1), np.uint8)
        img_dilate = cv2.dilate(threshold, kernel, iterations=1)
        img_erode = cv2.erode(img_dilate, kernel, iterations=1)
        img_empty[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = img_erode

    cv2.imshow('frame', image)
    cv2.imshow('frame2', img_empty)

    cv2.imwrite("image/" + str(i) + ".jpg", img_empty)


if not cap.isOpened():
    print('ERROR FILE NOT FOUND OR WRONG CODEC USED!')
i = 1
while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        # time.sleep(1 / fps)  # to run according to frame rate otherwise it go on highSpeed
        # convert BGR to GrayScale
        detectText(frame, i)
        i = 1 + i
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
