from ultralytics import YOLO

# model = YOLO('yolov8n.pt')
model = YOLO('best.pt')

model.predict(
   source='https://blog.kakaocdn.net/dn/cakZAB/btrxKhcpgaT/3xK4G4ko3cuDdlO8jxKOn0/img.jpg',
   conf=0.25,
   save=True,
   project="result"
)

