import cv2
import pre_processor

class frame_seperator:

    # input video file
    cap = cv2.VideoCapture('../../../FYP Videos/2.mp4')
    # get frame rate
    fps = cap.get(cv2.CAP_PROP_FPS)

    def __init__(self):
        pass

    def seperator(self, pre_processor_obj= pre_processor.pre_processor()):
        if not self.cap.isOpened():
            print('ERROR FILE NOT FOUND OR WRONG CODEC USED!')
        frame_position = 1
        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if ret:
                # time.sleep(1 / fps)  # to run according to frame rate otherwise it go on highSpeed
                pre_processor_obj.pre_processing(frame, frame_position)

                frame_position += 1
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        self.cap.release()




