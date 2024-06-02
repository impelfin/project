import requests
import os
import textwrap

def summarize_contents(contents_url, target_language):
    
    KAGI_API_TOKEN = os.environ["KAGI_API_TOKEN"] # Kagi API 키
    
    api_url = "https://kagi.com/api/v0/summarize"
    headers = {"Authorization": "Bot " + KAGI_API_TOKEN}
    parameters = {"url":contents_url, "target_language":target_language}

    r = requests.get(api_url, headers=headers, params=parameters)
    summary = r.json()['data']['output'] # 요약 내용을 별도의 변수에 할당
    
    return summary

contents_url = "https://www.youtube.com/watch?v=Ks-_Mh1QhMc"
target_language = "KO" # 요약할 언어를 한국어로 지정

try:
    summary = summarize_contents(contents_url, target_language)

    print("[콘텐츠 URL]", contents_url)
    print(textwrap.shorten(summary, 150 ,placeholder=' [..이하 생략..]')) # 축약 출력
    # print(summary) # 전체 출력
except:
    print("해당 URL의 내용을 요약하지 못했습니다. 다시 시도해 주세요.")
