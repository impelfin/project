import requests
import os 
import textwrap

KAGI_API_TOKEN = os.environ["KAGI_API_TOKEN"] # Kagi API 키

api_url = "https://kagi.com/api/v0/summarize"
contents_url = "https://edition.cnn.com/2023/03/26/middleeast/israel-judicial-overhaul-legislation-intl/index.html"
headers = {"Authorization": "Bot " + KAGI_API_TOKEN}
parameters = {"url":contents_url, "target_language":"KO"}

r = requests.get(api_url, headers=headers, params=parameters)

summary = r.json()['data']['output'] # 요약 내용을 별도의 변수에 할당

shorten_summary = textwrap.shorten(summary, 150, placeholder=' [..이하 생략..]')

print("- 요약 내용(축약):", shorten_summary) # 요약 내용(축약) 출력
# print("- 요약 내용:", summary) # 요약 내용(전체) 출력
