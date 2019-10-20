import cv2
import borderless_figure_detector


class unique_frame_detector:
    # object of borderless_figure_detector_class
    borderless_figure_detector_obj = borderless_figure_detector.figure_detector_borderless()

    # constructor
    def __init__(self):
        self.previous_image = None
        self.firstFrame = False
        self.skipCountBySize = 0
        self.skipCountByPixel = 0

    # method - to detect unique frame using localize text width changes and number of pixel value changes
    def detect_unique(self, img, img_empty, height, frame_position, time_stamp, max_width, max_width_x):
        # to be a suitable frame, max_width of a contour in a frame should larger than 180
        if max_width > 180:
            # check is this the first selected frame and set first values for previous_image
            if not self.firstFrame:

                self.firstFrame = True
                # crop text area using max_width and x value of max_width
                crop_img = img_empty[0:height, max_width_x:max_width_x + max_width]
                self.previous_image = crop_img

            else:
                # crop text area using max_width and x value of max_width
                crop_img = img_empty[0:height, max_width_x:max_width_x + max_width]
                # check dimensions of previous and current text regions
                if self.previous_image.shape == crop_img.shape:
                    # to avoid blur effect when changes the frames
                    self.skipCountByPixel += 1
                    if self.skipCountByPixel > 50:

                        self.skipCountByPixel = 0
                        self.skipCountBySize = 0
                        # get number of pixels of value 255
                        previous_image_NoneZeroPixel = cv2.countNonZero(self.previous_image)
                        current_image_NoneZeroPixel = cv2.countNonZero(crop_img)

                        height1, width1 = self.previous_image.shape
                        height2, width2 = crop_img.shape
                        # get number of pixels of value 255 - black pixels - text pixels
                        previous_image_ZeroPixel = height1 * width1 - previous_image_NoneZeroPixel
                        current_image_ZeroPixel = height2 * width2 - current_image_NoneZeroPixel

                        x = previous_image_ZeroPixel + 75
                        y = previous_image_ZeroPixel - 75
                        # to check changes inside same dimension text regions
                        if x < current_image_ZeroPixel or y > current_image_ZeroPixel:
                            self.previous_image = crop_img
                            # save binary and grey image in image directory
                            cv2.imwrite("image/" + str(frame_position - 50) + "-Pixel" + ".jpg", img)
                            cv2.imwrite("image/" + str(frame_position - 50) + "_2-Pixel" + ".jpg", img_empty)
                            # method call
                            self.borderless_figure_detector_obj.figure_detection_borderless(img, img_empty,
                                                                                            frame_position - 50,
                                                                                            time_stamp)
                # dimension are different in previous and current text region
                else:
                    # to avoid blur effect when changes the frames
                    self.skipCountBySize += 1

                    if self.skipCountBySize > 50:
                        self.skipCountByPixel = 0
                        self.skipCountBySize = 0

                        self.previous_image = crop_img
                        # save binary and grey image in image directory
                        cv2.imwrite("image/" + str(frame_position - 50) + "-Size" + ".jpg", img)
                        cv2.imwrite("image/" + str(frame_position - 50) + "_2-size" + ".jpg", img_empty)
                        # method call
                        self.borderless_figure_detector_obj.figure_detection_borderless(img, img_empty,
                                                                                        frame_position - 50, time_stamp)

        cv2.imshow("video", img)
