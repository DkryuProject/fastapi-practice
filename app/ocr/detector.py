from ultralytics import YOLO


class CardDetector:
    def __init__(self):
        self.model = YOLO("weights/card_detector.pt")

    def detect(self, image):
        result = self.model(image)[0]
        boxes = {}

        for b in result.boxes:
            cls = self.model.names[int(b.cls)]
            boxes[cls] = b.xyxy[0].tolist()

        return boxes

    def crop(self, image, box):
        x1, y1, x2, y2 = map(int, box)
        return image[y1:y2, x1:x2]
