import cv2
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

class text_extraction:

    def __init__(self):
        self.first = True
        self.previous_content = None

    def extract_text_string(self,image, frame_position):
        cv2.imshow("ocr_img", image)
        content = pytesseract.image_to_string(image, lang='eng')

        self.string_manipulation(content.strip(), frame_position)



    def string_manipulation(self, content, frame_position):

        if self.first:
            self.write_to_textfile(content, frame_position)
            self.first = False
            self.previous_content = content
        else:
            previous_trim_content = "".join(re.findall("[a-zA-Z]+", self.previous_content.lower()))
            current_trim_content = "".join(re.findall("[a-zA-Z]+", content.lower()))

            if previous_trim_content != current_trim_content:
                self.previous_content = content
                self.write_to_textfile(content, frame_position)



    def write_to_textfile(self,content,frame_position):
            f = open(str(frame_position) + ".txt", "w+")
            f.write("------------------------------------------------\n\n")
            f.write(content)
            f.write("\n\n------------------------------------------------\n\n")
            f.close()