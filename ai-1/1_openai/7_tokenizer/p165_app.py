import tiktoken

# 인코딩 획득
enc = tiktoken.get_encoding("cl100k_base")

# 인코딩 실행
tokens = enc.encode("Hello World!")
print(len(tokens))
print(tokens)

# 디코딩 실행
print(enc.decode(tokens))

# 분할된 상태에서 디코딩 실행
print(enc.decode_tokens_bytes(tokens))
