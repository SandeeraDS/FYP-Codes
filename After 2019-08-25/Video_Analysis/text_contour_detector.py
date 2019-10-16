import cv2
import numpy as np
import unique_frame_detector


class text_contour_detector:

    obj = unique_frame_detector.unque_frame_detector()

    def __init__(self):
        pass

    def contour_detection(self, img, img_dialate, frame_position):


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

        self.draw_contour(img, list, max_width, max_width_x,frame_position)


    def draw_contour(self, img, list, max_width, max_width_x,frame_position):

        height, width = img.shape
        img_empty = np.zeros([height, width], dtype=np.uint8)
        img_empty.fill(255)

        for r in list:
            blur = cv2.GaussianBlur(img[r[1]:r[1] + r[3], r[0]:r[0] + r[2]], (3, 3), 0)
            threshold = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 7)
            kernel = np.ones((1, 1), np.uint8)
            img_dilate = cv2.dilate(threshold, kernel, iterations=1)
            img_erode = cv2.erode(img_dilate, kernel, iterations=1)
            img_empty[r[1]:r[1] + r[3], r[0]:r[0] + r[2]] = img_erode


        self.obj.detect_unique(img, img_empty, height, frame_position, max_width, max_width_x)