import cv2

# input video file
cap = cv2.VideoCapture('../../../FYP Videos/114.mp4')
# get frame rate
fps = cap.get(cv2.CAP_PROP_FPS)

previous_image = None
firstFrame = False
skipCountBySize = 0
skipCountByPixel = 0


# method for text detecting


def detectText(image, number):
    height, width, channels = image.shape
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # linear contrast stretching
    minmax_img = cv2.normalize(img, 0, 255, norm_type=cv2.NORM_MINMAX)

    # Sobel
    sobel_img_x = cv2.Sobel(minmax_img, cv2.CV_8U, 1, 0, ksize=3)

    retval, threshold = cv2.threshold(sobel_img_x, 244, 255, cv2.THRESH_BINARY)

    # Dilation
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(10, 2), anchor=(-1, -1))
    img_dilate = cv2.morphologyEx(threshold, cv2.MORPH_DILATE, kernel, anchor=(-1, -1), iterations=2,
                                  borderType=cv2.BORDER_REFLECT, borderValue=255)

    # Find Contours
    im2, contours, hierarchy = cv2.findContours(img_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # GeaomatricalConstraints
    list = []
    max_width = 0
    max_width_x = 0

    for contour in contours:
        brect = cv2.boundingRect(contour)  # brect = (x,y,w,h)
        ar = brect[2] / brect[3]

        if ar > 2 and brect[2] > 40 and brect[3] > 20 and brect[3] < 100:
            list.append(brect)
            if (max_width < brect[2]):
                max_width = brect[2]
                max_width_x = brect[0]

    global previous_image
    global firstFrame
    global skipCountBySize
    global skipCountByPixel
    if max_width > 180:

        if not firstFrame:
            firstFrame = True
            # crop_img = threshold[0:height, max_width_x:max_width_x + max_width]
            crop_img = img[0:height, max_width_x:max_width_x + max_width]
            retval, crop_img = cv2.threshold(crop_img, 150, 255, cv2.THRESH_BINARY)
            previous_image = crop_img
            cv2.imwrite("image/" + str(count) + "-start" + ".jpg", crop_img)
            cv2.imshow("Changed", img)

        else:
            crop_img_gray = img[0:height, max_width_x:max_width_x + max_width]
            retval, crop_img = cv2.threshold(crop_img_gray, 150, 255, cv2.THRESH_BINARY)

            if previous_image.shape == crop_img.shape:
                skipCountByPixel += 1
                if skipCountByPixel > 40:
                    skipCountByPixel = 0
                    skipCountBySize = 0

                    previous_image_NoneZeroPixel = cv2.countNonZero(previous_image);
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
                        cv2.imwrite("image/" + str(count) + "-Pixel" + ".jpg", img)

                    # sift = cv2.xfeatures2d.SIFT_create()
                    #
                    # # find the keypoints and descriptors with SIFT
                    # kp1, des1 = sift.detectAndCompute(previous_image, None)
                    # kp2, des2 = sift.detectAndCompute(crop_img, None)
                    #
                    # # FLANN parameters
                    # FLANN_INDEX_KDTREE = 0
                    # index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
                    # search_params = dict()
                    #
                    # flann = cv2.FlannBasedMatcher(index_params, search_params)
                    #
                    # matches = flann.knnMatch(des1, des2, k=2)
                    #
                    # good_points = []
                    #
                    # # ratio test
                    # for match1, match2 in matches:
                    #     if match1.distance < 0.2 * match2.distance:
                    #         good_points.append(match1)
                    #
                    # goodPointRatio = (len(matches) * 40) / 100
                    #
                    # if goodPointRatio > len(good_points):
                    #     previous_image = crop_img
                    #     cv2.imwrite("image/" + str(count) + "-Pixel" + ".jpg", img)
                    #     cv2.imshow("PixelChange", img)

                    # cv2.imshow("PixelChange", crop_img)

            else:
                skipCountBySize += 1
                if skipCountBySize > 40:
                    skipCountBySize = 0
                    skipCountByPixel = 0
                    previous_image = crop_img
                    cv2.imwrite("image/" + str(count) + "-Size" + ".jpg", img)
                    cv2.imshow("Changed", img)

    cv2.imshow('frame', image)
    # cv2.imshow('frame2', img_dilate)


if not cap.isOpened():
    print('ERROR FILE NOT FOUND OR WRONG CODEC USED!')
count = 1
while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        # time.sleep(1 / fps)  # to run according to frame rate otherwise it go on highSpeed
        # convert BGR to GrayScale
        detectText(frame, count)
        count += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
