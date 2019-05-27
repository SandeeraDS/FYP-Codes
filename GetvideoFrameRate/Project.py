import cv2

cap = cv2.VideoCapture('../../FYP Videos/2.mp4')
# Frame rate
fps = cap.get(cv2.CAP_PROP_FPS)

print(fps)
# print number of frames
print(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# frame number
count = 1
frame_dict = {}
while cap.isOpened():
    frame_exists, curr_frame = cap.read()
    if frame_exists:

        # store frame name(count) and frame timestamp in dictionary(key value pair)
        frame_dict[count] = count/fps
        # save frames in folder
        cv2.imwrite("img/"+str(count)+".jpg", curr_frame)
        count += 1
    else:
        break

cap.release()

for key, value in frame_dict.items():
    print(key, "->", value)



