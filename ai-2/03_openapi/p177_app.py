import openai
from IPython.display import Image, display

response = openai.Image.create(
              prompt="Happy robots playing in the playground",
              n=2,
              size="512x512" # 이미지 크기를 512 x 512로 지정 
)

for data in response['data']:
    image_url = data['url'] # 이미지 URL 추출    
    # print(image_url[:170]) # 이미지 URL 일부 표시
    print(image_url) # 이미지 URL 전체 표시
    
    # display(Image(image_url, format='png')) # 이미지를 화면에 표시
               