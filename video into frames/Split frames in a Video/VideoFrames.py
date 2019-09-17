import cv2
import os

cap = cv2.VideoCapture('../../../FYP Videos/table_04.mp4')
# path = 'D:/OpenCV/Scripts/Images'

if cap.isOpened() == False:
    print('ERROR FILE NOT FOUND OR WRONG CODEC USED!')
count =1;

while cap.isOpened():
    ret, frame = cap.read()

    if ret == True:
        cv2.imwrite(str(count) + '.jpg', frame)
    count+=1

cap.release()
