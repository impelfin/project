import requests
import os 
import textwrap

KAGI_API_TOKEN = os.environ["KAGI_API_TOKEN"] # Kagi API 키

engines = ["cecil", "agnes", "daphne", "muriel"] # 엔진 전체

api_url = "https://kagi.com/api/v0/summarize"
contents_url = "https://www.khan.co.kr/culture/culture-general/article/202212310830021"
headers = {"Authorization": "Bot " + KAGI_API_TOKEN}

for engine in engines:
    parameters = {"url":contents_url, "engine":engine, "target_language":"KO"}

    r = requests.get(api_url, headers=headers, params=parameters)

    summary = r.json()['data']['output'] # 요약 내용을 별도의 변수에 할당

    shorten_summary = textwrap.shorten(summary, 150, placeholder=' [..이하 생략..]')
    
    print("[요약 엔진]", engine)
    print("- 요약 내용(축약):", shorten_summary) # 요약 내용(축약) 출력
    # print("- 요약 내용:", summary) # 요약 내용(전체) 출력
