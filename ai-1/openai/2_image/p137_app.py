import openai

# 이미지와 마스크 준비(현재 폴더에 이미지와 마스크를 넣어 둡니다)
image = open("image.png", "rb")
mask = open("mask.png", "rb")

# 이미지와 텍스트에서 이미지 편집을 실행
response = openai.Image.create_edit(
  image=image,
  mask=mask,
  prompt="many apples in cardboard box",
  n=1,
  size="512x512"
)
image_url = response["data"][0]["url"]
print(image_url)
