from ultralytics import YOLO

# model = YOLO('yolov8n.pt')
model = YOLO('best.pt')

model.predict(
   source='https://sateconomy.co.kr/news/data/20181123/p179589475849522_794.jpg',
   conf=0.25,
   save=True,
   project=".",
   name="result",
   exist_ok=True
)

