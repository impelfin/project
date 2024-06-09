import openai

# 프롬프트 준비
prompt = "인공지능에 대해 알려주세요."

# 텍스트 생성 실행
response = openai.Completion.create(
    model="gpt-3.5-turbo-instruct",
    prompt=prompt,
    temperature=0,
    max_tokens=500
)
print(response["choices"][0]["text"])
