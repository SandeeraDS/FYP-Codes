import cv2

cap = cv2.VideoCapture('../../FYP Videos/3.mp4')
# Frame rate
fps = cap.get(cv2.CAP_PROP_FPS)


count = 1;

while cap.isOpened():

    frame_exists, curr_frame = cap.read()
    if frame_exists:
        # Current position of the video file in milliseconds or video capture timestamp
        print(cap.get(cv2.CAP_PROP_POS_MSEC)/1000)
        if count == 1000:
            break
        count += 1

    else:
        break

print("number of frames = ", count)

print("duration using numberOfFrame/FPS = ", 1000/cap.get(cv2.CAP_PROP_FPS))

cap.release()
