import cv2
import numpy as np

img = 255*np.ones([500, 500], dtype=np.uint8)
cv2.imshow("img", img)
cv2.waitKey()