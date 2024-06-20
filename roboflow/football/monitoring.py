from fastapi import FastAPI, HTTPException, Depends
import boto3
from botocore.exceptions import NoCredentialsError
from datetime import timedelta, timezone
import os
from dotenv import load_dotenv
import asyncio
from roboflow import Roboflow
import json
import numpy as np
import shutil
import cv2
import subprocess
from ultralytics import YOLO

load_dotenv(dotenv_path='../../../.env')

app = FastAPI()

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('ID'),
    aws_secret_access_key=os.getenv('SECRET'),
    region_name=os.getenv('MYREGION')
)

BUCKET_NAME = os.getenv('BUCKET_NAME')
FOLDER_NAME = 'uploadedVideos/'

# KST 시간대 설정
KST = timezone(timedelta(hours=9))

rf = Roboflow(api_key=os.getenv("ROBOFLOW_API_KEY"))
project = rf.workspace().project("test_project-3cocv")
model = project.version(1).model

# YOLOv8 모델 로드
yolo_model = YOLO('yolov8s.pt')

# 필요한 클래스들만 정의 (0: person)
TARGET_CLASSES = [0]

class S3MonitorState:
    def __init__(self):
        self.previous_files = set()
        self.folder_detected = False
        self.monitoring = True  # 모니터링 상태를 나타내는 플래그

state = S3MonitorState()

@app.on_event("startup")
async def startup_event():
    # 주기적으로 폴더 확인
    asyncio.create_task(monitor_s3_folder(state))

async def monitor_s3_folder(state: S3MonitorState):
    while True:
        if state.monitoring:
            await check_s3_folder(state)
        await asyncio.sleep(1)

async def check_s3_folder(state: S3MonitorState):
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=FOLDER_NAME)
        if 'Contents' in response:
            current_files = set([content['Key'] for content in response['Contents']])
            if not current_files:
                print(f"No such folder: {FOLDER_NAME}")
                state.folder_detected = False
            else:
                if not state.folder_detected:
                    print(f"Folder {FOLDER_NAME} detected.")
                    state.folder_detected = True
                print(f"Files detected: {current_files}")

                new_files = current_files - state.previous_files

                if new_files:
                    print(f"New files detected: {new_files}")
                    state.monitoring = False  # 모니터링 중단
                    await process_new_files(new_files, state)
                    state.previous_files = current_files
        else:
            if state.folder_detected:
                print(f"Folder {FOLDER_NAME} not found.")
                state.folder_detected = False
            print(f"No such folder: {FOLDER_NAME}")
    except NoCredentialsError:
        print("Credentials not available")
        raise HTTPException(status_code=403, detail="Credentials not available")

async def process_new_files(new_files, state):
    tmp_folder = '/full/01_ldynamics/backend/opencv/tmp'
    frame_folder = os.path.join(tmp_folder, 'frames')
    
    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)
    if not os.path.exists(frame_folder):
        os.makedirs(frame_folder)

    for new_file in new_files:
        # S3에서 파일 다운로드
        file_path = os.path.join(tmp_folder, new_file.split('/')[-1])
        try:
            with open(file_path, 'wb') as f:
                s3.download_fileobj(BUCKET_NAME, new_file, f)
            print(f"Downloaded {new_file} to {file_path}")
        except Exception as e:
            print(f"Failed to download {new_file}: {e}")
            continue

        # 비디오 FPS 확인
        video_fps = get_video_fps(file_path)
        inference_fps = 5  # 적절한 inference_fps 설정
        if video_fps % inference_fps != 0:
            inference_fps = video_fps // (video_fps // inference_fps)
        print(f"Video FPS: {video_fps}, Inference FPS: {inference_fps}")

        # 파일 다운로드가 완료된 후 파일 경로를 API에 전달하여 작업 수행
        try:
            # Roboflow 모델을 사용하여 비디오 예측 수행
            prediction = model.predict_video(
                file_path,
                fps=inference_fps,
                prediction_type="batch-video",
            )

            # 반환된 값을 확인하고 적절히 처리
            print(f"Prediction response: {prediction}")

            # 예상되는 반환값 구조에 맞게 분리
            if isinstance(prediction, tuple) and len(prediction) >= 2:
                job_id = prediction[0]
                signed_url = prediction[1]
                print(f"Job ID: {job_id}, Signed URL: {signed_url}")

                # 비디오 예측 결과를 기다리고 처리
                results = model.poll_until_video_results(job_id)
                print(f"Video inference results: {results}")

                # 결과를 JSON 파일로 저장
                json_output_path = os.path.join(tmp_folder, 'results.json')
                with open(json_output_path, 'w') as json_file:
                    json.dump(results, json_file)
                print(f"Results saved to {json_output_path}")

                # YOLOv8 모델로 비디오 처리
                await process_video_yolo(file_path, frame_folder, video_fps, new_file)

            else:
                raise ValueError("Unexpected return value from predict_video")

        except Exception as e:
            print(f"Failed to process {file_path}: {e}")

    state.monitoring = True  # 모니터링 재개

def check_ffmpeg_installed():
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path is None:
        raise EnvironmentError("FFmpeg is not installed. Please install FFmpeg and try again.")
    return ffmpeg_path

def get_video_fps(file_path):
    ffmpeg_path = check_ffmpeg_installed()
    result = subprocess.run(
        [ffmpeg_path, "-i", file_path],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    output = result.stderr
    for line in output.split('\n'):
        if "fps" in line:
            parts = line.split(',')
            for part in parts:
                if "fps" in part:
                    fps = float(part.split()[0])
                    return fps
    return 30  # 기본값

async def process_video_yolo(file_path: str, frame_folder: str, video_fps: int, new_file: str):
    cap = cv2.VideoCapture(file_path)
    output_filename = os.path.basename(new_file).replace('.mp4', '_output.mp4')
    output_path = os.path.join('/full/01_ldynamics/backend/opencv/tmp', output_filename)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 15, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    # 이전 프레임 저장용 변수
    prev_frame = None

    frame_count = 0
    sample_rate = video_fps // 15  # 매 15프레임 중 하나의 프레임을 선택

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 프레임 샘플링
        if frame_count % sample_rate == 0:
            # 프레임의 일부분만 자르기 (위아래 범위 제한)
            height, width, _ = frame.shape
            top_crop = int(height * 0.1)  # 위에서 10% 자르기
            bottom_crop = int(height * 0.1)  # 아래에서 10% 자르기
            cropped_frame = frame[top_crop:height-bottom_crop, :]

            # YOLO 모델을 사용하여 오브젝트 감지 수행 (필요한 클래스만)
            results = yolo_model.predict(source=cropped_frame, conf=0.25, iou=0.65, classes=TARGET_CLASSES)

            # 움직임 감지를 위한 프레임 차이 계산
            if prev_frame is not None:
                frame_delta = cv2.absdiff(cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY), prev_frame)
                thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
                thresh = cv2.dilate(thresh, None, iterations=2)
                contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # 움직임이 있는 영역 찾기
                moving_areas = []
                for contour in contours:
                    if cv2.contourArea(contour) < 500:
                        continue
                    (x, y, w, h) = cv2.boundingRect(contour)
                    moving_areas.append((x, y, x + w, y + h))

                # 필터링된 클래스에 대해 바운딩 박스 그리기
                for result in results:
                    for box in result.boxes:
                        class_id = int(box.cls[0])
                        if class_id in TARGET_CLASSES:
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            conf = box.conf[0]
                            label = f'{yolo_model.names[class_id]}: {conf:.2f}'
                            # 움직임이 있는 영역 내에 있는지 확인
                            is_moving = any(x1 < mx2 and x2 > mx1 and y1 < my2 and y2 > my1 for mx1, my1, mx2, my2 in moving_areas)
                            if is_moving:
                                # 원본 프레임에 바운딩 박스 그리기
                                cv2.rectangle(frame, (x1, y1 + top_crop), (x2, y2 + top_crop), (255, 0, 0), 2)
                                cv2.putText(frame, label, (x1, y1 + top_crop - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            prev_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)

            # 결과 프레임을 비디오에 쓰기
            out.write(frame)

        frame_count += 1

    cap.release()
    out.release()

    print(f"YOLOv8 annotated video saved to {output_path}")

    # 프레임 파일 삭제
    shutil.rmtree(frame_folder)
    print(f"Temporary frames in {frame_folder} deleted.")

@app.get("/")
async def root(state: S3MonitorState = Depends(lambda: state)):
    if not state.folder_detected:
        return {"message": "Folder not yet detected"}

    return {"message": "File updated"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
