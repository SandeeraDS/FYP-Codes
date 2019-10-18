import cv2
import text_extraction

class figure_detector_border:

    text_extraction_obj = text_extraction.text_extraction()

    def __init__(self):
        self.first =True
        self.previous_h = 0
        self.previous_w = 0

    def figure_detection_border(self, gray_img, binary_img, frame_position):

        img = gray_img.copy()

        edges = cv2.Canny(img, 31, 180, apertureSize=3)

        im2, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        table_x = -1
        table_y = -1
        table_w = 450
        table_h = 200

        for contour in contours:
            # get rectangle bounding contour
            [x, y, w, h] = cv2.boundingRect(contour)
            # Don't plot small false positives that aren't text
            if (w > table_w and h > table_h):
                table_x = x
                table_y = y
                table_h = h
                table_w = w
        if not table_x == -1 and not table_y == -1:

            if self.first:
                cv2.rectangle(gray_img, (table_x, table_y), (table_x + table_w, table_y + table_h), (255, 0, 0), 2)
                cv2.imwrite("table/" + str(frame_position) + "-Size" + ".jpg", gray_img)
                self.first=False
                self.previous_h = table_h
                self.previous_w = table_w

            else:
                if self.previous_w == table_w or self.previous_h == table_h:
                        pass
                else:
                    cv2.rectangle(gray_img, (table_x, table_y), (table_x + table_w, table_y + table_h), (255, 0, 0), 2)
                    cv2.imwrite("table/" + str(frame_position) + "-Size" + ".jpg", gray_img)
                    self.previous_h = table_h
                    self.previous_w = table_w
        else:
             self.text_extraction_obj.extract_text_string(binary_img, frame_position)