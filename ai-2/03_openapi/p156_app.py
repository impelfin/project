import openai
import os

# API 키 설정
openai.api_key = os.environ["OPENAI_API_KEY"]

# 모든 OpenAP API의 모델 리스트를 요청해 가져오기
models = openai.Model.list()

# 가져온 모델 리스트 출력하기 
# print(models["data"])  # 모델 리스트 전체 정보 출력
print(models["data"][0]['id']) # 모델 리스트 중 첫 번째 항목의 ID 출력
