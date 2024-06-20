from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import Any
import requests
import subprocess
import os
import shutil
import json

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
    temp_output_dir = os.path.join(process_temp_dir, 'output')

    if not os.path.exists(temp_output_dir):
        os.makedirs(temp_output_dir)

    try:
        with open(temp_input_path, 'wb') as temp_input:
            temp_input.write(await file.read())

        # 동영상을 10초 단위로 분할
        subprocess.run(['ffmpeg', '-i', temp_input_path, '-c', 'copy', '-map', '0', '-segment_time', '10', '-f', 'segment','-start_number', '1', os.path.join(temp_output_dir, 'segment_%03d.mp4')], check=True)

        segment_files = sorted([os.path.join(temp_output_dir, f) for f in os.listdir(temp_output_dir) if f.startswith('segment_') and f.endswith('.mp4')])
        total_time = 0

        for segment_index, segment_file in enumerate(segment_files):
            segment_output_dir = os.path.join(temp_output_dir, f'segment_{segment_index+1:03d}')

            if not os.path.exists(segment_output_dir):
                os.makedirs(segment_output_dir)

            # 각 세그먼트에서 프레임을 JPEG 형식으로 추출
            fps = 25  # 원하는 fps 값
            subprocess.run(['ffmpeg', '-i', segment_file, '-r', str(fps), os.path.join(segment_output_dir, 'frame_%04d.jpg')], check=True)

            # 각 프레임에 대해 객체 감지 수행
            frame_files = sorted([os.path.join(segment_output_dir, f) for f in os.listdir(segment_output_dir) if f.startswith('frame_') and f.endswith('.jpg')])
            segment_detections = {}

            for i, frame_file in enumerate(frame_files):
                # 프레임의 타임스탬프 계산
                timestamp = total_time + (i * (1 / fps))
                minutes = int(timestamp // 60)
                seconds = int(timestamp % 60)
                milliseconds = int((timestamp % 1) * 1000)
                timestamp_str = f'{minutes:02}:{seconds:02}.{milliseconds:03}'

                with open(frame_file, 'rb') as f:
                    image_data = f.read()
                files = {"file": image_data}
                response = requests.post(f"{API_URL}/{MODEL_ID}", files=files, params={"api_key": API_KEY})

                if response.status_code == 200:
                    frame_detections = response.json()['predictions']
                    segment_detections[timestamp_str] = frame_detections

            # 감지 결과를 JSON 텍스트 파일로 저장
            result_file_path = os.path.join( f'segment_{segment_index+1:03d}.txt')
            with open(result_file_path, 'w') as result_file:
                json.dump(segment_detections, result_file, indent=4)

            # 다음 세그먼트를 위해 total_time 업데이트
            total_time += len(frame_files) * (1 / fps)

        # 결과 JSON 파일 경로 반환
        return {"result_files": [os.path.join( f'segment_{segment_index+1:03d}.txt') for segment_index in range(len(segment_files))]}

    finally:
        # 임시 파일 및 디렉토리 정리
        if os.path.exists(process_temp_dir):
            shutil.rmtree(process_temp_dir)
