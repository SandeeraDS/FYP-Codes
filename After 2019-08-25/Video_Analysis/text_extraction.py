import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

class text_extraction:

    def __init__(self):
        pass

    def extract_text_string(self,image, frame_position):
        cv2.imshow("ocr_img", image)
        result = pytesseract.image_to_string(image, lang='eng')
        f = open(str(frame_position) + ".txt", "w+")
        f.write("------------------------------------------------\n\n")
        f.write(result)
        f.write("\n\n------------------------------------------------\n\n")
        f.close()
