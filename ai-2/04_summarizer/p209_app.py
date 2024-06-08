import requests
import os
import textwrap

# 1) 텍스트 파일에서 데이터 가져오기
text_file_name = "./스티브_잡스_2005_스탠포드_연설.txt" # 영어 문장 텍스트 파일

with open(text_file_name, 'r', encoding='utf-8') as f: # 텍스트 파일을 읽기 모드로 열기
    text_data = f.read() # 텍스트 파일의 내용을 읽어서 text_data에 할당

print("[원본 텍스트 파일의 내용 앞부분만 출력]")
print(text_data[:290])
print()

# 2) 텍스트 데이터 요약하기
KAGI_API_TOKEN = os.environ["KAGI_API_TOKEN"] # Kagi API 키

api_url = "https://kagi.com/api/v0/summarize"
headers = {"Authorization": "Bot " + KAGI_API_TOKEN}
data = {"text":text_data}
# data = {"text":text_data, "target_language":"KO"} # 요약의 출력 언어를 한국어로 지정
r = requests.post(api_url, headers=headers, data=data)

summary = r.json()['data']['output'] # 요약 내용을 별도의 변수에 할당
shorten_summary = textwrap.shorten(summary, 250, placeholder=' [..이하 생략..]')

print("[요약 내용 출력]")
print(shorten_summary) # 요약 내용(축약) 출력
# print(summary) # 요약 내용(전체) 출력
