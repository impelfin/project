from ultralytics import YOLO

# model = YOLO('yolov8n.pt')
model = YOLO('best.pt')

model.predict(
   source='snac2.png',
   conf=0.25,
   save=True,
   project=".",
   name="result",
   exist_ok=True
)

