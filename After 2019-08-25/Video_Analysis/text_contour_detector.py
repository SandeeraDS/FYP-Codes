import cv2
import numpy as np
import unique_frame_detector


class text_contour_detector:
    # object of unique frame detector class
    obj = unique_frame_detector.unique_frame_detector()

    # constructor
    def __init__(self):
        pass

    # method - detect contours in pre-processed frame and select suitable contours for text
    def contour_detection(self, img, img_dialate, frame_position, time_stamp):

        # Find Contours
        im2, contours, hierarchy = cv2.findContours(img_dialate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_list = []
        max_width = 0
        max_width_x = 0

        for contour in contours:
            # Calculates the up-right bounding rectangle of a point set
            brect = cv2.boundingRect(contour)  # brect = (x,y,w,h)
            ar = brect[2] / brect[3]

            # localize text based on following conditions
            if ar >= 2.7 and brect[2] >= 40 and 17 <= brect[3] <= 60:
                contours_list.append(brect)
                # catch width and x value of widest rectangle in the particular frame
                if max_width < brect[2]:
                    max_width = brect[2]
                    max_width_x = brect[0]
        # method call
        self.separate_contour(img, contours_list, max_width, max_width_x, frame_position, time_stamp)

    # method - mark selected contour in blank image
    def separate_contour(self, img, contours_list, max_width, max_width_x, frame_position, time_stamp):
        # get height and width of current frame
        height, width = img.shape
        # create a blank image using dimension of frame to store content get from contour
        img_empty = np.zeros([height, width], dtype=np.uint8)
        img_empty.fill(255)
        gray_blank_img = np.ones([height, width], dtype=np.uint8)
        gray_blank_img.fill(255)
        # set localize text into blank image-so now no effect of person
        for r in contours_list:
            # pre-processing for localized text
            blur = cv2.GaussianBlur(img[r[1]:r[1] + r[3], r[0]:r[0] + r[2]], (3, 3), 0)
            threshold = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 7)
            kernel = np.ones((1, 1), np.uint8)
            img_dilate = cv2.dilate(threshold, kernel, iterations=1)
            img_erode = cv2.erode(img_dilate, kernel, iterations=1)
            # set to blank image with correct place
            img_empty[r[1]:r[1] + r[3], r[0]:r[0] + r[2]] = img_erode
            gray_blank_img[r[1]:r[1] + r[3], r[0]:r[0] + r[2]] = img[r[1]:r[1] + r[3], r[0]:r[0] + r[2]]
        # method call
        # cv2.imshow("grayScale",gray_blank_img)
        self.obj.detect_unique(img, img_empty, height, frame_position, time_stamp, max_width, max_width_x,gray_blank_img)
