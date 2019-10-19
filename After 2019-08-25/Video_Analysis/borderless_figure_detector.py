import cv2
import text_extraction
import border_figure_detector


class figure_detector_borderless:
    text_extraction_obj = text_extraction.text_extraction()
    border_figure_detector_obj = border_figure_detector.figure_detector_border()

    def __init__(self):
        self.first = True
        self.previous_h = 0
        self.previous_w = 0

    def figure_detection_borderless(self, gray_img, binary_img, frame_position, time_stamp):
        img = gray_img.copy()
        height, width = gray_img.shape
        pre_processed = self.pre_process_image(img)
        text_boxes = self.find_text_boxes(pre_processed)
        cells = self.find_table_in_boxes(text_boxes)
        hor_lines, ver_lines = self.build_lines(cells)
        [min_x, min_y, max_x, max_y] = self.get_main_points(hor_lines, ver_lines, gray_img)

        if min_x == -100 and min_y == -100 and max_x == -100 and max_y == -100:
            self.border_figure_detector_obj.figure_detection_border(gray_img, binary_img, frame_position, time_stamp)
        else:

            if self.first:
                cv2.imwrite("table/" + str(frame_position) + ".jpg",
                            gray_img[min_y:max_y, min_x:max_x])

                self.first = False
                self.previous_h = max_y - min_y
                self.previous_w = max_x - min_x
                self.text_extraction_obj.extract_text_string(binary_img[0:min_y, 0:width], frame_position, time_stamp)

            else:
                if self.previous_w == max_x - min_x or self.previous_h == max_y - min_y:
                    pass
                else:
                    cv2.imwrite("table/" + str(frame_position) + ".jpg",
                                gray_img[min_y:max_y, min_x:max_x])
                    self.previous_h = max_y - min_y
                    self.previous_w = max_x - min_x
                    self.text_extraction_obj.extract_text_string(binary_img[0:min_y, 0:width], frame_position,
                                                                 time_stamp)

    def pre_process_image(self, img):
        # linear contrast stretching
        minmax_img = cv2.normalize(img, 0, 255, norm_type=cv2.NORM_MINMAX)
        # Sobel
        sobel_img_x = cv2.Sobel(minmax_img, cv2.CV_8U, 1, 0, ksize=3)
        # thresholding
        retval, threshold = cv2.threshold(sobel_img_x, 96, 255, cv2.THRESH_BINARY)
        # Dilation
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(14, 3), anchor=(-1, -1))
        img_dilate = cv2.morphologyEx(threshold, cv2.MORPH_DILATE, kernel, anchor=(-1, -1), iterations=3,
                                      borderType=cv2.BORDER_REFLECT, borderValue=255)

        return img_dilate

    def find_text_boxes(self, pre, min_text_height_limit=15, max_text_height_limit=60):
        # Looking for the text spots contours
        # OpenCV 3
        # img, contours, hierarchy = cv2.findContours(pre, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # OpenCV 4
        im2, contours, hierarchy = cv2.findContours(pre, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # Getting the texts bounding boxes based on the text size assumptions
        boxes = []
        for contour in contours:
            box = cv2.boundingRect(contour)
            h = box[3]

            if min_text_height_limit < h < max_text_height_limit:
                boxes.append(box)
        return boxes

    def find_table_in_boxes(self, boxes, min_columns=2):
        rows = {}
        cols = {}

        # Clustering the bounding boxes by their positions
        for box in boxes:
            (x, y, w, h) = box
            col_key = x  # cell_threshold
            row_key = y  # // cell_threshold
            cols[row_key] = [box] if col_key not in cols else cols[col_key] + [box]
            rows[row_key] = [box] if row_key not in rows else rows[row_key] + [box]

        # Filtering out the clusters having less than 2 cols
        table_cells = list(filter(lambda r: len(r) >= min_columns, rows.values()))
        # Sorting the row cells by x coord
        table_cells = [list(sorted(tb)) for tb in table_cells]
        # Sorting rows by the y coord
        table_cells = list(sorted(table_cells, key=lambda r: r[0][1]))
        return table_cells

    def build_lines(self, table_cells):
        if table_cells is None or len(table_cells) <= 0:
            return [], []

        max_last_col_width_row = max(table_cells, key=lambda b: b[-1][2])
        max_x = max_last_col_width_row[-1][0] + max_last_col_width_row[-1][2]

        max_last_row_height_box = max(table_cells[-1], key=lambda b: b[3])
        max_y = max_last_row_height_box[1] + max_last_row_height_box[3]

        hor_lines = []
        ver_lines = []

        for box in table_cells:
            x = box[0][0]
            y = box[0][1]
            hor_lines.append((x, y, max_x, y))

        for box in table_cells[0]:
            x = box[0]
            y = box[1]
            ver_lines.append((x, y, x, max_y))

        (x, y, w, h) = table_cells[0][-1]
        ver_lines.append((max_x, y, max_x, max_y))
        (x, y, w, h) = table_cells[0][0]
        hor_lines.append((x, max_y, max_x, max_y))

        return hor_lines, ver_lines

    def get_main_points(self, hor_lines, ver_lines, vis):
        final_box = []
        if len(ver_lines) > 2 and not ver_lines[0][3] - ver_lines[0][1] < 150:
            final_box.append(ver_lines[0])
            final_box.append(ver_lines[len(ver_lines) - 1])

        if len(hor_lines) > 2 and len(final_box) != 0 and not (hor_lines[0][2] - hor_lines[0][0] < 150):
            final_box.append(hor_lines[0])
            final_box.append(hor_lines[len(hor_lines) - 1])


        else:
            return [-100, -100, -100, -100]

        min_x = 2000000
        min_y = 2000000
        max_x = -1
        max_y = -1

        if len(final_box) == 4:
            for line in final_box:
                [x1, y1, x2, y2] = line

                if min_x > x1:
                    min_x = x1
                if min_x > x2:
                    min_x = x2
                if max_x < x1:
                    max_x = x1
                if max_x < x2:
                    max_x = x2

                if min_y > y1:
                    min_y = y1
                if min_y > y2:
                    min_y = y2
                if max_y < y1:
                    max_y = y1
                if max_y < y2:
                    max_y = y2

            return [min_x, min_y, max_x, max_y]
