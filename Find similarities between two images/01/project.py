import cv2
import numpy as np

original = cv2.imread("01.jpg")
duplicate = cv2.imread("02.jpg")

# b,g,r = cv2.split(original)


image01 = original.shape
image02 = duplicate.shape

print(image01)
print(image02)

if original.shape == duplicate.shape:

    difference = cv2.subtract(src1=original, src2=duplicate)

    gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    print(gray)
    print(cv2.countNonZero(gray))
    if cv2.countNonZero(gray)==0:
        print("Both Same")

    # cv2.imshow("difference",difference)

# cv2.imshow('img1', original)
# cv2.imshow('img2', duplicate)


cv2.waitKey(0)
cv2.destroyAllWindows()
