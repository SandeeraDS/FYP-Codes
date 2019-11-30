import cv2

cap = cv2.VideoCapture('../../../FYP Videos/table_05.mp4')

if cap.isOpened() is False:
    print('ERROR FILE NOT FOUND OR WRONG CODEC USED!')
count = 1

while cap.isOpened():
    ret, frame = cap.read()

    if ret is True:
        cv2.imwrite("image/" + str(count) + ".jpg", frame)
    count += 1

cap.release()
