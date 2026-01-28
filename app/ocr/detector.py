import cv2
import numpy as np


class CardDetector:
    def detect_card(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 대비 강화 (실무 핵심)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        gray = clahe.apply(gray)

        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blur, 30, 120)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        edged = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(
            edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        h, w = image.shape[:2]
        image_area = h * w

        candidates = []

        for cnt in contours:
            x, y, bw, bh = cv2.boundingRect(cnt)
            area = bw * bh
            aspect = bw / float(bh)

            # 카드 비율 범위 확장 (실무값)
            if (
                    1.2 < aspect < 2.1 or
                    0.45 < aspect < 0.85
            ):
                if area > image_area * 0.08:
                    candidates.append((area, (x, y, x + bw, y + bh)))

        # 1차: 카드 비율 후보 중 가장 큰 것
        if candidates:
            return max(candidates, key=lambda x: x[0])[1]

        # 🔥 2차 fallback: 가장 큰 사각형
        max_box = None
        max_area = 0

        for cnt in contours:
            x, y, bw, bh = cv2.boundingRect(cnt)
            area = bw * bh
            if area > max_area:
                max_area = area
                max_box = (x, y, x + bw, y + bh)

        if max_area > image_area * 0.12:
            return max_box

        return None

    def crop(self, image, box):
        if box is None:
            return None
        x1, y1, x2, y2 = map(int, box)
        return image[y1:y2, x1:x2]
