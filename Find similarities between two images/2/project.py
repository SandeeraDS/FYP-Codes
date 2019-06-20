import cv2
import numpy as np

# original = cv2.imread("14.jpg")
# duplicate = cv2.imread("862.jpg")


original = cv2.imread("1929.jpg")
duplicate = cv2.imread("1437.jpg")

original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
duplicate = cv2.cvtColor(duplicate, cv2.COLOR_BGR2GRAY)

height1, width1= original.shape
height2, width2 = duplicate.shape

# print(width1)
# print(width2)

# original = cv2.normalize(original, 0, 255, norm_type=cv2.NORM_MINMAX)
# duplicate = cv2.normalize(duplicate, 0, 255, norm_type=cv2.NORM_MINMAX)

# original = cv2.Sobel(original, cv2.CV_8U, 1, 0, ksize=3)
# duplicate = cv2.Sobel(duplicate, cv2.CV_8U, 1, 0, ksize=3)

retval, original = cv2.threshold(original, 150, 255, cv2.THRESH_BINARY)
retval, duplicate = cv2.threshold(duplicate, 150, 255, cv2.THRESH_BINARY)

# print(cv2.countNonZero(original))
# print(cv2.countNonZero(duplicate))

cv2.imshow("img1", original)
cv2.imshow("img2", duplicate)
# cv2.imshow("img4", original_1)


# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(original, None)
kp2, des2 = sift.detectAndCompute(duplicate, None)

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict()

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1, des2, k=2)

print(len(kp1))
print(len(kp2))
print(len(matches))

good_points = []

# ratio test
for match1, match2 in matches:
    if match1.distance < 0.2 * match2.distance:
        good_points.append(match1)

print(len(good_points))
flann_matches = cv2.drawMatches(original, kp1, duplicate, kp2, good_points, None)

cv2.imshow("img3", flann_matches)

cv2.waitKey(0)
cv2.destroyAllWindows()
