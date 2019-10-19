import cv2
import borderless_figure_detector


class unque_frame_detector:
    borderless_figure_detector_obj = borderless_figure_detector.figure_detector_borderless()

    def __init__(self):
        self.previous_image = None
        self.firstFrame = False
        self.skipCountBySize = 0
        self.skipCountByPixel = 0

    def detect_unique(self, img, img_empty, height, frame_position, time_stamp, max_width, max_width_x):

        if max_width > 180:

            if not self.firstFrame:

                self.firstFrame = True
                crop_img = img_empty[0:height, max_width_x:max_width_x + max_width]
                self.previous_image = crop_img

            else:
                crop_img = img_empty[0:height, max_width_x:max_width_x + max_width]
                if self.previous_image.shape == crop_img.shape:

                    self.skipCountByPixel += 1

                    if self.skipCountByPixel > 50:

                        self.skipCountByPixel = 0
                        self.skipCountBySize = 0

                        previous_image_NoneZeroPixel = cv2.countNonZero(self.previous_image)
                        current_image_NoneZeroPixel = cv2.countNonZero(crop_img)

                        height1, width1 = self.previous_image.shape
                        height2, width2 = crop_img.shape

                        previous_image_ZeroPixel = height1 * width1 - previous_image_NoneZeroPixel
                        current_image_ZeroPixel = height2 * width2 - current_image_NoneZeroPixel

                        x = previous_image_ZeroPixel + 75
                        y = previous_image_ZeroPixel - 75

                        if x < current_image_ZeroPixel or y > current_image_ZeroPixel:
                            self.previous_image = crop_img
                            # cv2.imshow("result", img)
                            cv2.imwrite("image/" + str(frame_position - 50) + "-Pixel" + ".jpg", img)
                            cv2.imwrite("image/" + str(frame_position - 50) + "_2-Pixel" + ".jpg", img_empty)
                            self.borderless_figure_detector_obj.figure_detection_borderless(img, img_empty,
                                                                                            frame_position - 50,
                                                                                            time_stamp)
                else:

                    self.skipCountBySize += 1

                    if self.skipCountBySize > 50:
                        self.skipCountByPixel = 0
                        self.skipCountBySize = 0

                        self.previous_image = crop_img
                        # cv2.imshow("result", img)
                        cv2.imwrite("image/" + str(frame_position - 50) + "-Size" + ".jpg", img)
                        cv2.imwrite("image/" + str(frame_position - 50) + "_2-size" + ".jpg", img_empty)
                        self.borderless_figure_detector_obj.figure_detection_borderless(img, img_empty,
                                                                                        frame_position - 50, time_stamp)

        cv2.imshow("video", img)
