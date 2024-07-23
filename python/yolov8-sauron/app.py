from ultralytics import YOLO
import torch

# model = YOLO('yolov8n.pt')
model = YOLO('best10.pt')

device = torch.device("mps")

model.predict(
   source='https://img.hankyung.com/photo/202112/01.28350624.1.jpg',
   conf=0.25,
   save=True,
   project=".",
   name="result",
   exist_ok=True,
   device=device
)

