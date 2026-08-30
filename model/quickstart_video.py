from ultralytics import YOLO

model = YOLO("yolov8n.pt")
model.predict(source="model/videos/teste.mp4", show=True, conf=0.5, save=True)