import openai

# 프롬프트 준비
prompt = "cat dancing on car"

# 텍스트에서 이미지 생성 실행
response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="512x512"
)
image_url = response["data"][0]["url"]
print(image_url)

print(response)
