import requests
import os 

KAGI_API_TOKEN = os.environ["KAGI_API_TOKEN"] # Kagi API 키

contents_url = "https://www.youtube.com/watch?v=BmYv8XGl-YU"
url = f"https://kagi.com/api/v0/summarize?url={contents_url}" # 전달할 매개 변수를 URL에 포함
headers = {"Authorization": "Bot " + KAGI_API_TOKEN}

r = requests.get(url, headers=headers)
# print(r)

# print(r.json())

summary = r.json()['data']['output'] # 요약 내용을 별도의 변수에 할당
print(summary)
