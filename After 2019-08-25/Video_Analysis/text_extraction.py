import cv2
import pytesseract
import re
import Shared.frame_dict_ops as ops

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


class text_extraction:
    ops_obj = ops.dict_ops()

    def __init__(self):
        self.first = True
        self.previous_content = None

    def extract_text_string(self, image, frame_position, time_stamp):
        cv2.imshow("ocr_img", image)
        content = pytesseract.image_to_string(image, lang='eng')

        if len(content) > 4:
            self.string_manipulation(content.strip(), frame_position, time_stamp)

    def string_manipulation(self, content, frame_position, time_stamp):

        if self.first:
            self.write_to_textfile(content, frame_position, time_stamp)
            self.first = False
            self.previous_content = content
        else:
            previous_trim_content = "".join(re.findall("[a-zA-Z]+", self.previous_content.lower()))
            current_trim_content = "".join(re.findall("[a-zA-Z]+", content.lower()))

            if previous_trim_content != current_trim_content:
                self.previous_content = content
                self.write_to_textfile(content, frame_position, time_stamp)

    def write_to_textfile(self, content, frame_position, time_stamp):
        f = open(str(frame_position) + ".txt", "w+")
        f.write("------------------------------------------------\n\n")
        f.write(content)
        f.write("\n\n------------------------------------------------\n\n")
        f.close()
        self.ops_obj.add_to_dict_from_text_extract(frame_position, content, time_stamp)
