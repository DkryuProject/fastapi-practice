from paddleocr import PaddleOCR


class CardOCR:
    def __init__(self):
        self.ocr = PaddleOCR(
            lang="en",
            use_angle_cls=True,
            show_log=False
        )

    def read(self, image):
        result = self.ocr.ocr(image, cls=True)
        texts = []

        for line in result[0]:
            texts.append(line[1][0])

        return " ".join(texts)
