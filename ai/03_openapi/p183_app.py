import openai
from IPython.display import Image, display

org_image_file = "./data/org_image_for_variation.png" # 원본 이미지

# 이미지 변형 생성
response = openai.Image.create_variation( 
                image=open(org_image_file, "rb"),                         
                n=1, # 생성할 이미지 개수 지정
                size="256x256" # 생성할 이미지의 크기 지정                          
)
    
image_url = response['data'][0]['url']
print(image_url)

# print("[원본 이미지]")
# display(Image(org_image_file, format='png', width=256, height=256)) # 이미지를 화면에 표시
# print("[생성 이미지]")
# display(Image(image_url, format='png')) # 이미지를 화면에 표시
