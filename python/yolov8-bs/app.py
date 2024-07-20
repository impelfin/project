from ultralytics import YOLO

# model = YOLO('yolov8n.pt')
model = YOLO('best.pt')

model.predict(
   # source='https://godomall.speedycdn.net/2ac6be74e4add1400a2d415ea74927c8/goods/1000000942/image/main/1000000942_main_088.jpg',
   source='beverage3.png',
   conf=0.25,
   save=True,
   project=".",
   name="result",
   exist_ok=True
)

