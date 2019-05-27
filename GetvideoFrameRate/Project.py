import cv2

cap2 = cv2.VideoCapture('../../FYP Videos/1.mp4')
# Frame rate
fps2 = cap2.get(cv2.CAP_PROP_FPS)

print(fps2)
count = 1;#frame number

while(cap2.isOpened()):
    frame_exists, curr_frame = cap2.read()
    if frame_exists:
        print(count/fps2) #get relavant time of
        count += 1
    else:
        break

cap2.release()



