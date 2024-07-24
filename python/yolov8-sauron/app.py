from ultralytics import YOLO
import torch

# model = YOLO('yolov8n.pt')
model = YOLO('best.pt')

device = torch.device("mps")

model.predict(
   source='8_63.jpg',
   conf=0.25,
   save=True,
   project=".",
   name="result",
   exist_ok=True,
   device=device
)

