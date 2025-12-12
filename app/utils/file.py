import hashlib
import os
from fastapi import UploadFile

UPLOAD_DIR = "uploads"
ALLOWED_EXT = {"pdf", "png", "jpg", "jpeg"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def get_file_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def validate_file(file: UploadFile, content: bytes):
    ext = file.filename.split(".")[-1].lower()

    if ext not in ALLOWED_EXT:
        raise ValueError("허용되지 않은 파일 확장자입니다.")

    if len(content) > MAX_FILE_SIZE:
        raise ValueError("파일 크기가 제한을 초과했습니다.")

    return ext


def save_file(content: bytes, file_hash: str, ext: str) -> str:
    folder = UPLOAD_DIR
    os.makedirs(folder, exist_ok=True)

    save_name = f"{file_hash}.{ext}"
    file_path = os.path.join(folder, save_name)

    with open(file_path, "wb") as f:
        f.write(content)

    return file_path
