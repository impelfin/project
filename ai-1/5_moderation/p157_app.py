import openai

# 모더레이션 이용
response = openai.Moderation.create(
    input="I'll kill you!"
)

print(response)
