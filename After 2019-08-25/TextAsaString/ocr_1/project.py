import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
img = cv2.imread("j.jpg")

# img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# retval, threshold = cv2.threshold(img_gray, 120, 255, cv2.THRESH_BINARY)
# kernel = np.ones((1, 1), np.uint8)
# img_dilate = cv2.dilate(threshold, kernel, iterations=2)
# img_erode = cv2.erode(img_dilate, kernel, iterations=1)
#
# img_1 = np.zeros([512, 512, 1], dtype=np.uint8)
# img_1.fill(255)
result = pytesseract.image_to_string(img, lang='eng')
cv2.imshow("img1", img)
# cv2.imshow("img2", threshold)
# cv2.imshow("img3", img_1)

print(result)

f = open("guru99.txt", "w+")
f.write(result)
f.close()


cv2.waitKey(0)
