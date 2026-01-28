# app/ocr/easyocr_reader.py
from paddleocr import PaddleOCR


class CardOCR:
    def __init__(self):
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang="en",
        )

    def read(self, image):
        result = self.ocr.ocr(image)
        texts = []

        if not result:
            return texts

        for line in result:
            for item in line:
                text = item[1][0]
                score = item[1][1]

                if score > 0.6:
                    texts.append(text)

        return texts
