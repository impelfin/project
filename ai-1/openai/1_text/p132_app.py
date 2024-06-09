import openai

# 채팅 메시지 리스트 준비
messages = [
    {"role": "system", "content": "오타를 수정해 주세요."},
    {"role": "user", "content": "오늘은 정말 즐거웠따."},
]

# 편집 실행
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    temperature=0
)
print(response)
print()
print(response["choices"][0]["message"]["content"])

