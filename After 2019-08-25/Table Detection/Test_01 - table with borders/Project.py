import cv2
import numpy as np

img = cv2.imread("21.jpg")

# sobel_img_x = cv2.Sobel(img, cv2.CV_8U, 1, 0, ksize=3)
# sobel_img_y = cv2.Sobel(img, cv2.CV_8U, 0, 1, ksize=3)
# sobel = cv2.addWeighted(sobel_img_x, 1, sobel_img_y, 1, 0)

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#blur = cv2.GaussianBlur(img, (7, 7), 0)
# linear contrast stretching
#minmax_img = cv2.normalize(img, 0, 255, norm_type=cv2.NORM_MINMAX)
# Sobel
# sobel_img_x = cv2.Sobel(minmax_img, cv2.CV_8U, 1, 0, ksize=3)
# sobel_img_y = cv2.Sobel(minmax_img, cv2.CV_8U, 0, 1, ksize=3)
# sobel = cv2.addWeighted(sobel_img_x, 2, sobel_img_y, 2, 0)
edges = cv2.Canny(img, 31, 180, apertureSize = 3)
#retval, threshold = cv2.threshold(edges, 127, 255, 0)

im2, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
table_x = -1
table_y = -1
table_w = 450
table_h = 200
for contour in contours:
    # get rectangle bounding contour
    [x, y, w, h] = cv2.boundingRect(contour)
    # Don't plot small false positives that aren't text
    if (w >table_w and h> table_h):
        table_x = x
        table_y = y
        table_h = h
        table_w = w
if not table_x == -1 and not table_y == -1:
    cv2.rectangle(img, (table_x, table_y), (table_x + table_w, table_y + table_h), (0, 0, 0), 2)

cv2.imshow("img1", edges)
cv2.imshow("img2", img)
cv2.waitKey(0)
