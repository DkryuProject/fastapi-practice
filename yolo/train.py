from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("yolov8n.pt")  # 사전학습 모델
    model.train(
        data="card.yaml",
        epochs=50,
        imgsz=640,
        batch=8,
        cache=False
    )
