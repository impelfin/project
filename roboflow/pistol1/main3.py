from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import Any
import requests
import subprocess
import os
import shutil

app = FastAPI()

API_URL = "https://detect.roboflow.com"
API_KEY = "qyMDu2uErA0xG41LFgXI"
MODEL_ID = "pistol-nxy4n/1"

@app.post("/infer/")
async def infer_image(file: UploadFile = File(...)) -> Any:
    try:
        image_data = await file.read()
        files = {"file": image_data}
        response = requests.post(f"{API_URL}/{MODEL_ID}", files=files, params={"api_key": API_KEY})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/infer_video/")
async def infer_video(file: UploadFile = File(...)) -> Any:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    process_temp_dir = os.path.join(base_dir, "process_temp")

    if not os.path.exists(process_temp_dir):
        os.makedirs(process_temp_dir)

    temp_input_path = os.path.join(process_temp_dir, 'input.mp4')
    temp_output_path = os.path.join(process_temp_dir, 'output.mp4')

    try:
        with open(temp_input_path, 'wb') as temp_input:
            temp_input.write(await file.read())

        # 동영상의 각 프레임을 JPEG 형식으로 추출
        fps = 10  # 원하는 fps 값으로 설정
        subprocess.run(['ffmpeg', '-i', temp_input_path, '-r', str(fps), os.path.join(process_temp_dir, 'frame_%04d.jpg')], check=True)

        # 각 프레임에 대해 객체 감지 및 사각형 그리기
        frame_files = sorted([os.path.join(process_temp_dir, f) for f in os.listdir(process_temp_dir) if f.startswith('frame_') and f.endswith('.jpg')])
        for i, frame_file in enumerate(frame_files):
            with open(frame_file, 'rb') as f:
                image_data = f.read()
            files = {"file": image_data}
            response = requests.post(f"{API_URL}/{MODEL_ID}", files=files, params={"api_key": API_KEY})

            if response.status_code == 200:
                detections = response.json()['predictions']
                drawbox_filter = ""
                for detection in detections:
                    x = detection["x"]
                    y = detection["y"]
                    width = detection["width"]
                    height = detection["height"]
                    x1 = int(x - width / 2)
                    y1 = int(y - height / 2)
                    x2 = int(x + width / 2)
                    y2 = int(y + height / 2)
                    drawbox_filter += f"drawbox=x={x1}:y={y1}:w={x2-x1}:h={y2-y1}:color=red@0.5:t=5,"

                if drawbox_filter:
                    output_frame_file = os.path.join(process_temp_dir, f'boxed_frame_{i:04d}.jpg')
                    # 프레임에 사각형 그리기
                    subprocess.run(['ffmpeg', '-i', frame_file, '-vf', drawbox_filter[:-1], '-frames:v', '1', output_frame_file], check=True)
                else:
                    os.rename(frame_file, os.path.join(process_temp_dir, f'boxed_frame_{i:04d}.jpg'))

        # 사각형이 그려진 프레임을 다시 동영상으로 합치기
        subprocess.run(['ffmpeg', '-framerate', str(fps), '-i', os.path.join(process_temp_dir, 'boxed_frame_%04d.jpg'), '-vcodec', 'libx264', '-pix_fmt', 'yuv420p', temp_output_path], check=True)

        # 결과 동영상 파일 경로 반환
        return {"video_path": temp_output_path}

    finally:
        # 임시 파일 및 디렉토리 삭제
        if os.path.exists(process_temp_dir):
            shutil.rmtree(process_temp_dir)

