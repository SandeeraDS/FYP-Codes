import cv2
import pre_processor
import Shared.frame_dict_ops as ops


class frame_seperator:
    # input video file
    cap = cv2.VideoCapture('../../../FYP Videos/table_04.mp4')
    # get frame rate
    fps = cap.get(cv2.CAP_PROP_FPS)
    # create object of frame detail operation class
    ops_obj = ops.dict_ops()

    # constructor
    def __init__(self):
        pass

    # method - separate video into frames
    def seperator(self, pre_processor_obj=pre_processor.pre_processor()):

        if not self.cap.isOpened():
            print('ERROR FILE NOT FOUND OR WRONG CODEC USED!')

        frame_position = 1  # get first frame of the video as 1

        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if ret:
                # get timestamp of current frame
                time_stamp = self.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                # sent frame to pre-processing
                pre_processor_obj.pre_processing(frame, frame_position, time_stamp)

                frame_position += 1
                # condition for hard stop the separating to frames
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                # method call
                self.iterate_different_frame_timestamp()
                break

        self.cap.release()

    # method - to  iterate selected frame's details
    def iterate_different_frame_timestamp(self):
        self.ops_obj.view_dict()
