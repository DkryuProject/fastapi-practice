import cv2
import random
import os
import numpy as np
import math

W, H = 856, 540  # 기본 카드 (가로)

def random_card_number():
    return "".join([str(random.randint(0, 9)) for _ in range(16)])

def random_expiry():
    return f"{random.randint(1,12):02d}/{random.randint(25,30)}"

def rotate(img, boxes, angle):
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)

    img_rot = cv2.warpAffine(img, M, (w, h))

    new_boxes = []
    rad = np.deg2rad(angle)

    for cls, x, y, bw, bh in boxes:
        # YOLO → pixel
        px, py = x * w, y * h
        bw_px, bh_px = bw * w, bh * h

        cx, cy = w / 2, h / 2
        dx, dy = px - cx, py - cy

        nx = dx * np.cos(rad) - dy * np.sin(rad) + cx
        ny = dx * np.sin(rad) + dy * np.cos(rad) + cy

        new_boxes.append((cls, nx / w, ny / h, bw_px / w, bh_px / h))

    return img_rot, new_boxes

def draw_card(img, labels):
    number = " ".join(random_card_number()[i:i+4] for i in range(0,16,4))
    expiry = random_expiry()

    num_x, num_y = random.randint(80,150), random.randint(280,340)
    exp_x, exp_y = num_x, num_y + 60

    cv2.putText(img, number, (num_x, num_y),
                cv2.FONT_HERSHEY_SIMPLEX, 1.6, (255,255,255), 3)
    cv2.putText(img, expiry, (exp_x, exp_y),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 2)

    labels.append((0, (num_x+300)/W, (num_y-30)/H, 600/W, 60/H))
    labels.append((1, (exp_x+90)/W, (exp_y-20)/H, 180/W, 40/H))

def generate(split, count):
    os.makedirs(f"dataset/images/{split}", exist_ok=True)
    os.makedirs(f"dataset/labels/{split}", exist_ok=True)

    for i in range(count):
        img = np.full((H, W, 3), random.randint(20,60), dtype=np.uint8)
        labels = []

        draw_card(img, labels)

        # 🔥 회전 (가로 / 세로 대응)
        angle = random.choice([0, 90, -90, random.randint(-10, 10)])
        img, labels = rotate(img, labels, angle)

        cv2.imwrite(f"dataset/images/{split}/{i}.jpg", img)

        with open(f"dataset/labels/{split}/{i}.txt", "w") as f:
            for cls, x, y, w, h in labels:
                f.write(f"{cls} {x} {y} {w} {h}\n")

if __name__ == "__main__":
    generate("train", 1200)
    generate("val", 300)
