from fastapi import APIRouter, UploadFile, File
import cv2
import numpy as np

from .detector import CardDetector
from .easyocr_reader import CardOCR
from .postprocess import normalize_card_number, luhn_check

router = APIRouter()

detector = CardDetector()
ocr = CardOCR()


@router.post("/card")
async def read_card(file: UploadFile = File(...)):
    image_bytes = await file.read()
    npimg = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    box = detector.detect_card(image)

    if box:
        x1, y1, x2, y2 = box
        cv2.rectangle(image, (x1,y1), (x2,y2), (0,255,0), 2)
        cv2.imwrite("debug_detected.jpg", image)

    if box is None:
        return {
            "success": False,
            "message": "Card not detected",
            "data": None
        }

    card_img = detector.crop(image, box)
    raw_text = ocr.read(card_img)

    card_number = normalize_card_number(raw_text)

    if len(card_number) not in (15, 16):
        return {
            "success": False,
            "message": "Invalid card number length",
            "data": None
        }

    if not luhn_check(card_number):
        return {
            "success": False,
            "message": "Card number not valid",
            "data": None
        }

    return {
        "success": True,
        "data": {
            "card_number": card_number
        }
    }
