import openai

# 임베딩을 생성할 텍스트 준비
text = "이것은 테스트입니다."

# 텍스트로부터 임베딩 생성
response = openai.Embedding.create(
    input=text, 
    model="text-embedding-ada-002"
)

# 확인
print(len(response["data"][0]["embedding"]))
print(response["data"][0]["embedding"])

print(response)
