from ultralytics import YOLO

# model = YOLO('yolov8n.pt')
model = YOLO('best.pt')

model.predict(
   source='https://cdn.bizwnews.com/news/photo/202406/84655_90881_153.jpg',
   conf=0.25,
   save=True,
   project=".",
   name="result",
   exist_ok=True
)

