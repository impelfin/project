import openai

# 프롬프트 준비
prompt = '''한국어를 영어로 번역합니다.

한국어: 나는 고양이다
영어:'''

import openai

# 텍스트 생성 실행
response = openai.Completion.create(
    model="gpt-3.5-turbo-instruct",
    prompt=prompt,
    temperature=0
)
print(response["choices"][0]["text"])

