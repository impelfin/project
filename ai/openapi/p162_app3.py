import openai
import json

# 대화 메시지 정의
messages = [
    {"role": "user", "content": "한글은 언제 만들어졌나요?"}
]

# Chat Completions API 호출
response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=1000,
                temperature=0.8,
                n=2 
)

print("응답 개수:", len(response.choices)) # 응답 개수 출력

print("[응답 0]", response.choices[0].message['content'])
print("[응답 1]", response.choices[1].message['content'])
