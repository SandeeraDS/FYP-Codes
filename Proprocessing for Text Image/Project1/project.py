import cv2
import numpy as np

img = cv2.imread("1.jpg")

height, width, channels = img.shape

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img_gray_2 = img_gray.copy()

img_gray_2 = cv2.adaptiveThreshold(img_gray_2, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 3,18)
thresh = img_gray_2.copy()

kernel = np.ones(shape=(5,5),dtype=np.float32)/25
# dst = cv2.filter2D(thresh,-1,kernel)
dst = cv2.GaussianBlur(thresh,(5,5),10)
# gradient Magnitude
sobel_img_x = cv2.Sobel(dst, cv2.CV_8U, 1, 0, ksize=3)

min = sobel_img_x.min()
max = sobel_img_x.max()

# for i in range(height):
#     for j in range(width):
#         y = ((sobel_img_x[i, j] - min) / (max - min)) * 255
#         sobel_img_x[i, j] = y

# histogram equalization
hist_img = cv2.equalizeHist(sobel_img_x)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(10, 3), anchor=(-1, -1))
img_dilate = cv2.morphologyEx(hist_img, cv2.MORPH_DILATE, kernel, anchor=(-1, -1), iterations=2,
                              borderType=cv2.BORDER_REFLECT, borderValue=255)
# Find Contours
contours, hierarchy = cv2.findContours(img_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# GeaomatricalConstraints
list = []
for contour in contours:
    brect = cv2.boundingRect(contour)  # brect = (x,y,w,h)
    ar = brect[2] / brect[3]

    if ar > 2 and brect[2] > 40 and brect[3] > 16 and brect[3] < 100:
        list.append(brect)

for r in list:
    # draw region of interest
    cv2.rectangle(img, (r[0], r[1]), (r[0] + r[2], r[1] + r[3]), (250, 0, 0), 2)

cv2.imshow("Original", img)
cv2.imshow("Preprocessed", hist_img)
cv2.imshow("Threshhold", img_dilate)
# print(result)


cv2.waitKey(0)
