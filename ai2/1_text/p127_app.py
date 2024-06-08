import openai

# 프롬프트 준비
prompt = '''# "Hello World!" 표시
def helloworld():
'''

# 텍스트 생성 실행
response = openai.Completion.create(
    model="gpt-3.5-turbo-instruct",
    prompt=prompt,
    temperature=0
)
print(response["choices"][0]["text"])
