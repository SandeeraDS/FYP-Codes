import cv2
import numpy as np

import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
# input video file
cap = cv2.VideoCapture('../../../../FYP Videos/table_04.mp4')
# get frame rate
fps = cap.get(cv2.CAP_PROP_FPS)

previous_image = None
firstFrame = False
skipCountBySize = 0
skipCountByPixel = 0

# method for text detecting

def extract_text_string(image, frame_position):


    cv2.imshow("ocr_img", image)
    result = pytesseract.image_to_string(image, lang='eng')
    f = open(str(frame_position)+".txt", "w+")
    f.write("------------------------------------------------\n\n")
    f.write(result)
    f.write("\n\n------------------------------------------------\n\n")
    f.close()

def detect_text(img, img_dialate, frame_position):
    
    height, width = img.shape
    draw = img
    # empty image(white image)
    img_empty = np.zeros([height, width], dtype=np.uint8)
    img_empty.fill(255)
    # Find Contours
    im2, contours, hierarchy = cv2.findContours(img_dialate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # GeometricalConstraints
    list = []
    max_width = 0
    max_width_x = 0

    for contour in contours:
        brect = cv2.boundingRect(contour)  # brect = (x,y,w,h)
        ar = brect[2] / brect[3]

        if ar >= 2.7 and brect[2] >= 40 and brect[3] >= 17 and brect[3] <= 60:
            list.append(brect)
            if max_width < brect[2]:
                max_width = brect[2]
                max_width_x = brect[0]
    for r in list:
        #cv2.rectangle(draw, (r[0], r[1]), (r[0] + r[2], r[1] + r[3]), (250, 0, 0), 2)
        blur = cv2.GaussianBlur(img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]], (3, 3), 0)
        threshold = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 7)
        kernel = np.ones((1, 1), np.uint8)
        img_dilate = cv2.dilate(threshold, kernel, iterations=1)
        img_erode = cv2.erode(img_dilate, kernel, iterations=1)
        img_empty[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = img_erode

    global previous_image
    global firstFrame
    global skipCountBySize
    global skipCountByPixel
    if max_width > 180:

        if not firstFrame:

            firstFrame = True
            crop_img = img_empty[0:height, max_width_x:max_width_x + max_width]
            # retval, crop_img =cv2.threshold(crop_img, 150, 255, cv2.THRESH_BINARY)
            previous_image = crop_img
            # cv2.imwrite("image/" + str(frame_position) + "-start" + ".jpg", crop_img)
            #cv2.imshow("Changed", img_empty)

        else:
            crop_img = img_empty[0:height, max_width_x:max_width_x + max_width]
            if previous_image.shape == crop_img.shape:

                skipCountByPixel += 1

                if skipCountByPixel > 100:

                    skipCountByPixel = 0
                    skipCountBySize = 0

                    previous_image_NoneZeroPixel = cv2.countNonZero(previous_image)
                    current_image_NoneZeroPixel = cv2.countNonZero(crop_img)

                    height1, width1 = previous_image.shape
                    height2, width2 = crop_img.shape

                    previous_image_ZeroPixel = height1 * width1 - previous_image_NoneZeroPixel
                    current_image_ZeroPixel = height2 * width2 - current_image_NoneZeroPixel

                    x = previous_image_ZeroPixel + 75
                    y = previous_image_ZeroPixel - 75

                    if x < current_image_ZeroPixel or y > current_image_ZeroPixel:
                        previous_image = crop_img
                        cv2.imshow("Changed", img)
                        cv2.imwrite("image/" + str(frame_position - 100) + "-Pixel" + ".jpg", img)
                        cv2.imwrite("image/" + str(frame_position - 100) + "_2-Pixel" + ".jpg", img_empty)
                        extract_text_string(img_empty,frame_position-100)
            else:

                skipCountBySize += 1

                if skipCountBySize > 50:
                    skipCountByPixel = 0
                    skipCountBySize = 0

                    # previous_image_NoneZeroPixel = cv2.countNonZero(previous_image)
                    # current_image_NoneZeroPixel = cv2.countNonZero(crop_img)
                    #
                    # height1, width1 = previous_image.shape
                    # height2, width2 = crop_img.shape
                    #
                    # previous_image_ZeroPixel = height1 * width1 - previous_image_NoneZeroPixel
                    # current_image_ZeroPixel = height2 * width2 - current_image_NoneZeroPixel
                    #
                    # x = previous_image_ZeroPixel + 50
                    # y = previous_image_ZeroPixel - 50
                    #
                    # if x < current_image_ZeroPixel or y > current_image_ZeroPixel:
                    #     previous_image = crop_img
                    #     cv2.imshow("Changed", img)
                    #     cv2.imwrite("image/" + str(frame_position - 50) + "-size" + ".jpg", img)
                    #     cv2.imwrite("image/" + str(frame_position - 50) + "_2-size" + ".jpg", img_empty)
                    #     extract_text_string(img_empty, frame_position)
                    # skipCountBySize = 0
                    # skipCountByPixel = 0
                    previous_image = crop_img
                    cv2.imwrite("image/" + str(frame_position-50) + "-Size" + ".jpg", img)
                    cv2.imwrite("image/" + str(frame_position - 50) + "_2-size" + ".jpg", img_empty)
                    extract_text_string(img_empty, frame_position-50)

    cv2.imshow('frame', img)
    #cv2.imshow("draw", draw)


def pre_processing(image, frame_position):

    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # linear contrast stretching
    minmax_img = cv2.normalize(img, 0, 255, norm_type=cv2.NORM_MINMAX)
    # Sobel
    sobel_img_x = cv2.Sobel(minmax_img, cv2.CV_8U, 1, 0, ksize=3)
    # thresholding
    retval, threshold = cv2.threshold(sobel_img_x, 244, 255, cv2.THRESH_BINARY)
    # Dilation
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(11, 2), anchor=(-1, -1))
    img_dilate = cv2.morphologyEx(threshold, cv2.MORPH_DILATE, kernel, anchor=(-1, -1), iterations=2,
                                  borderType=cv2.BORDER_REFLECT, borderValue=255)
    detect_text(img, img_dilate, frame_position)


if not cap.isOpened():
    print('ERROR FILE NOT FOUND OR WRONG CODEC USED!')
frame_position = 1
while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        # time.sleep(1 / fps)  # to run according to frame rate otherwise it go on highSpeed
        # convert BGR to GrayScale
        pre_processing(frame, frame_position)
        frame_position += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
