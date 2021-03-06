import cv2


# This only works if there's only one table on a page
# Important parameters:
#  - morph_size
#  - min_text_height_limit
#  - max_text_height_limit
#  - cell_threshold
#  - min_columns


def pre_process_image(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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
    cv2.imshow("pre_processsing", img_dilate)
    return img_dilate


# Clustering the bounding boxes by their positions
def find_text_boxes(pre, img, min_text_height_limit=17, max_text_height_limit=50):
    # Looking for the text spots contours
    # OpenCV 3
    # img, contours, hierarchy = cv2.findContours(pre, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # OpenCV 4
    new_img = ~img
    im2, contours, hierarchy = cv2.findContours(pre, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Getting the texts bounding boxes based on the text size assumptions
    boxes = []
    for contour in contours:
        box = cv2.boundingRect(contour)
        h = box[3]
        # check box are satisfy those height conditions
        if min_text_height_limit < h < max_text_height_limit:
            boxes.append(box)
    for r in boxes:
        # draw region of interest
        cv2.rectangle(new_img, (r[0], r[1]), (r[0] + r[2], r[1] + r[3]), (250, 0, 0), 2)
    cv2.imshow("countor", new_img)
    return boxes


def find_table_in_boxes(boxes, min_columns=2):
    rows = {}
    cols = {}

    # Clustering the bounding boxes by their positions
    for box in boxes:
        (x, y, w, h) = box
        col_key = x  # cell_threshold
        row_key = y  # // cell_threshold
        # if cols not contain the cols key then add to cols dict(add new element)
        # if key is already contain, then append it.
        # cols[col_key] = [box] if col_key not in cols else cols[col_key] + [box]
        # if rows not contain the raw_key then add to cols dict(add new element)
        # if key is already contain, then append it.
        rows[row_key] = [box] if row_key not in rows else rows[row_key] + [box]

    # Filtering out the clusters having less than 2 cols
    # values() is an inbuilt method in Python programming language that returns a
    # list of all the values available in a given dictionary.
    # filter(function, sequence)
    # function is checking min cols and sequence is raw value
    # r is one element, example = [(642, 513, 83, 30), (216, 513, 144, 30)]
    table_cells = list(filter(lambda r: len(r) >= min_columns, rows.values()))
    # Sorting the row cells by x coord
    # do sorting inside a one element, one element can contain 2 or more box values
    # ex = [(642, 513, 83, 30), (216, 513, 144, 30)] --> [(216, 513, 144, 30), (642, 513, 83, 30)]
    table_cells = [list(sorted(tb)) for tb in table_cells]
    # Sorting rows by the y coord
    # do sorting respect to all the elements by x value of the element
    # before sort by y
    # [[(216, 513, 144, 30), (642, 513, 83, 30)], [(217, 408, 185, 32), (643, 408, 131, 32)],
    # [(216, 305, 161, 31), (643, 305, 122, 31)], [(214, 238, 217, 35), (644, 238, 179, 35)]]
    # after sort by y
    # [[(214, 238, 217, 35), (644, 238, 179, 35)], [(216, 305, 161, 31), (643, 305, 122, 31)],
    # [(217, 408, 185, 32), (643, 408, 131, 32)], [(216, 513, 144, 30), (642, 513, 83, 30)]]
    table_cells = list(sorted(table_cells, key=lambda r: r[0][1]))
    return table_cells


def build_lines(table_cells):
    if table_cells is None or len(table_cells) <= 0:
        return [], []
    print(table_cells)
    # get the element list with max w value
    max_last_col_width_row = max(table_cells, key=lambda b: b[-1][2])
    # here get the sum of x+w of max_last_col_width_row
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


# img = cv2.imread("12.jpg")
# img = cv2.imread("15.jpg")
img = cv2.imread("12.jpg")
# img = cv2.imread("07.jpg")
# img = cv2.imread("11.jpg")


pre_processed = pre_process_image(img)
text_boxes = find_text_boxes(pre_processed, img)
cells = find_table_in_boxes(text_boxes)
hor_lines, ver_lines = build_lines(cells)

# Visualize the result
vis = img.copy()
final_box = []
if len(ver_lines) > 2 and not ver_lines[0][3] - ver_lines[0][1] < 150:
    final_box.append(ver_lines[0])
    final_box.append(ver_lines[len(ver_lines) - 1])
    print("if 1")

if len(hor_lines) > 2 and len(final_box) != 0 and not (hor_lines[0][2] - hor_lines[0][0] < 150):
    final_box.append(hor_lines[0])
    final_box.append(hor_lines[len(hor_lines) - 1])
    print("if 2")

else:
    print("exit")

min_x = 2000000
min_y = 2000000
max_x = -1
max_y = -1

if len(final_box) == 4:
    for line in final_box:
        [x1, y1, x2, y2] = line

        # if min_x > x1:
        #     min_x = x1
        # if min_x > x2:
        #     min_x = x2
        # if max_x < x1:
        #     max_x = x1
        # if max_x < x2:
        #     max_x = x2
        #
        # if min_y > y1:
        #     min_y = y1
        # if min_y > y2:
        #     min_y = y2
        # if max_y < y1:
        #     max_y = y1
        # if max_y < y2:
        #     max_y = y2

        # print("final")
        cv2.line(vis, (x1, y1), (x2, y2), (255, 0, 0), 2)
        # break

# cv2.line(vis, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)
# cv2.rectangle(vis, (min_x, min_y-15), (max_x, max_y+10), (255, 0, 0), 2)
# cv2.imshow("img2", vis[min_y:max_y, min_x:max_x])
cv2.imshow("img2", vis)
cv2.waitKey(0)
