import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
img = cv2.imread("a.jpg")

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 7)
# minmax_img = cv2.normalize(img_gray, 0, 255, norm_type=cv2.NORM_MINMAX)


# retval, threshold = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
# kernel = np.ones((1, 1), np.uint8)
# img_dilate = cv2.dilate(threshold, kernel, iterations=1)
# img_erode = cv2.erode(img_dilate, kernel, iterations=1)


result = pytesseract.image_to_string(img, lang='eng')
cv2.imshow("raw", th3)
# cv2.imshow("img1", threshold)
# cv2.imshow("img2", img_dilate)
print(result)

cv2.waitKey(0)
