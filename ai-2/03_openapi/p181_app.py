import openai
from IPython.display import Image, display
from pathlib import Path

org_image_file = "./data/org_image_for_edit.png"   # 원본 이미지
mask_image_file = "./data/mask_image_for_edit.png" # 마스크 이미지

# 이미지 편집 생성 
response = openai.Image.create_edit( 
                image=open(org_image_file, "rb"), 
                mask=open(mask_image_file, "rb"),
                prompt="Happy robots swimming in the water",                           
                n=1, # 생성할 이미지 개수 지정
                size="256x256" # 생성할 이미지의 크기 지정                            
)

image_url = response['data'][0]['url'] # 생성 이미지 URL
print(image_url)

# print("[원본 이미지]")
# display(Image(org_image_file, format='png', width=256, height=256)) # 이미지를 화면에 표시
# print("[마스크 이미지]")
# display(Image(mask_image_file, format='png', width=256, height=256)) # 이미지를 화면에 표시
# print("[생성 이미지]")
# display(Image(image_url, format='png')) # 이미지를 화면에 표시
