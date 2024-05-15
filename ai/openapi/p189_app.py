import tiktoken

text = "tiktoken is great!" # 원본 텍스트
enc = tiktoken.get_encoding("cl100k_base")
# enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

encoded_list = enc.encode(text) # 텍스트 인코딩해 인코딩 리스트 생성
token_num = len(encoded_list)   # 인코딩 리스트의 길이로 토큰 개수 계산
decoded_text = enc.decode(encoded_list) # 인코딩 결과를 디코딩해서 텍스트 복원

print("- 인코딩 결과:", encoded_list)
print("- 토큰 개수:", token_num)
print("- 디코딩 결과:", decoded_text)
