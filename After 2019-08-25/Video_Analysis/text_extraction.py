import cv2
import pytesseract
import re
import Shared.frame_dict_ops as ops

# for use ocr library
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


class text_extraction:
    # add details to frame details dictionary
    # method call
    ops_obj = ops.dict_ops()

    # constructor
    def __init__(self):
        self.first = True
        self.previous_content = None

    # method - using ocr library get the text content of the image
    def extract_text_string(self, image, frame_position, time_stamp):
        content = pytesseract.image_to_string(image, lang='eng')
        # content should have at least 4 characters
        if len(content) > 4:
            # method call
            self.string_manipulation(content.strip(), frame_position, time_stamp)

    # method - identify similar frame content to identify unique content frame
    def string_manipulation(self, content, frame_position, time_stamp):

        if self.first:
            self.write_to_text_file(content, frame_position, time_stamp)
            self.first = False
            self.previous_content = content
        else:
            # compare only using alphabetic characters
            previous_trim_content = "".join(re.findall("[a-zA-Z]+", self.previous_content.lower()))
            current_trim_content = "".join(re.findall("[a-zA-Z]+", content.lower()))
            # compare with previous frame content
            if previous_trim_content != current_trim_content:
                self.previous_content = content
                self.write_to_text_file(content, frame_position, time_stamp)

    # method - write to content to a text file
    def write_to_text_file(self, content, frame_position, time_stamp):
        f = open(str(frame_position) + ".txt", "w+")
        f.write("------------------------------------------------\n\n")
        f.write(content)
        f.write("\n\n------------------------------------------------\n\n")
        f.close()
        # add details to frame details dictionary
        # method call
        self.ops_obj.add_to_dict_from_text_extract(frame_position, content, time_stamp)
