import openai
from IPython.display import Image, display
from pathlib import Path
import requests

# 디렉터리 경로를 입력해 path 객체를 생성
dir_path = Path('./data') # 내려받을 폴더 생성   

# 디렉터리가 없다면 생성
dir_path.mkdir(parents=True, exist_ok=True)

response = openai.Image.create(
              prompt="Happy robots playing in the playground",
              n=2,
              size="512x512" # 이미지 크기를 512 x 512로 지정 
)

for data in response['data']:
    image_url = data['url'] # 이미지 URL 추출
    
    image_filenme = image_url.split("?")[0].split("/")[-1]  # 이미지 파일 이름 추출   
    image_path = dir_path + image_filenme # 다운로드 파일의 경로 생성
    print("이미지 파일 경로:", image_path)
    
    r = requests.get(image_url) # 이미지 URL을 이용해 이미지 가져오기
    with open(image_path, 'wb') as f: # 가져온 이미지를 바이너리 파일로 저장
        f.write(r.content)
