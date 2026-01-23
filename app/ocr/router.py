from fastapi import APIRouter, UploadFile, File, HTTPException
from .detector import CardDetector
from .easyocr_reader import CardOCR
from .postprocess import parse_card_number
from .image import read_image

router = APIRouter()
detector = CardDetector()
ocr = CardOCR()

@router.post("/scan")
async def scan_card(file: UploadFile = File(...)):
    image = read_image(await file.read())

    boxes = detector.detect(image)
    if "card_number" not in boxes:
        raise HTTPException(400, "Card number not detected")

    crop = detector.crop(image, boxes["card_number"])
    text = ocr.read(crop)

    result = parse_card_number(text)
    if not result:
        raise HTTPException(422, "Invalid card number")

    return result
