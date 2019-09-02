import cv2

# input video file
cap = cv2.VideoCapture('../../../../FYP Videos/2.mp4')
# get frame rate
fps = cap.get(cv2.CAP_PROP_FPS)

previous_image = None
firstFrame = False
skipCountBySize = 0
skipCountByPixel = 0


# method for text detecting


def detect_text(img, img_dialate, frame_position):
    
    height, width = img.shape
    # Find Contours
    im2, contours, hierarchy = cv2.findContours(img_dialate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # GeometricalConstraints
    list = []
    max_width = 0
    max_width_x = 0

    for contour in contours:
        brect = cv2.boundingRect(contour)  # brect = (x,y,w,h)
        ar = brect[2] / brect[3]

        if ar > 2 and brect[2] > 40 and brect[3] > 20 and brect[3] < 100:
            list.append(brect)
            if max_width < brect[2]:
                max_width = brect[2]
                max_width_x = brect[0]

    global previous_image
    global firstFrame
    global skipCountBySize
    global skipCountByPixel
    if max_width > 180:

        if not firstFrame:

            firstFrame = True
            crop_img = img[0:height, max_width_x:max_width_x + max_width]
            retval, crop_img =cv2.threshold(crop_img, 150, 255, cv2.THRESH_BINARY)
            previous_image = crop_img
            cv2.imwrite("image/" + str(frame_position) + "-start" + ".jpg", crop_img)
            cv2.imshow("Changed", img)

        else:
            crop_img_gray = img[0:height, max_width_x:max_width_x + max_width]

            retval, crop_img = cv2.threshold(crop_img_gray, 150, 255, cv2.THRESH_BINARY)

            if previous_image.shape == crop_img.shape:

                skipCountByPixel += 1

                if skipCountByPixel > 40:

                    skipCountByPixel = 0
                    skipCountBySize = 0

                    previous_image_NoneZeroPixel = cv2.countNonZero(previous_image)
                    current_image_NoneZeroPixel = cv2.countNonZero(crop_img)

                    height1, width1 = previous_image.shape
                    height2, width2 = crop_img.shape

                    previous_image_ZeroPixel = height1 * width1 - previous_image_NoneZeroPixel
                    current_image_ZeroPixel = height2 * width2 - current_image_NoneZeroPixel

                    x = previous_image_ZeroPixel + 100
                    y = previous_image_ZeroPixel - 100

                    if x < current_image_ZeroPixel or y > current_image_ZeroPixel:
                        previous_image = crop_img
                        cv2.imshow("Changed", img)
                        cv2.imwrite("image/" + str(frame_position) + "-Pixel" + ".jpg", img)
            else:

                skipCountBySize += 1

                if skipCountBySize > 40:
                    skipCountBySize = 0
                    skipCountByPixel = 0
                    previous_image = crop_img
                    cv2.imwrite("image/" + str(frame_position) + "-Size" + ".jpg", img)
                    cv2.imshow("Changed", img)

    cv2.imshow('frame', img)


def pre_processing(image, frame_position):

    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # linear contrast stretching
    minmax_img = cv2.normalize(img, 0, 255, norm_type=cv2.NORM_MINMAX)
    # Sobel
    sobel_img_x = cv2.Sobel(minmax_img, cv2.CV_8U, 1, 0, ksize=3)
    # thresholding
    retval, threshold = cv2.threshold(sobel_img_x, 244, 255, cv2.THRESH_BINARY)
    # Dilation
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(10, 2), anchor=(-1, -1))
    img_dilate = cv2.morphologyEx(threshold, cv2.MORPH_DILATE, kernel, anchor=(-1, -1), iterations=2,
                                  borderType=cv2.BORDER_REFLECT, borderValue=255)
    detect_text(img, img_dilate, frame_position)


if not cap.isOpened():
    print('ERROR FILE NOT FOUND OR WRONG CODEC USED!')
frame_position = 1
while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        # time.sleep(1 / fps)  # to run according to frame rate otherwise it go on highSpeed
        # convert BGR to GrayScale
        pre_processing(frame, frame_position)
        frame_position += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
