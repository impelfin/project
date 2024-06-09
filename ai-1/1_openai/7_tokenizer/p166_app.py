import tiktoken

# 인코딩 획득
enc = tiktoken.get_encoding("cl100k_base")

# 인코딩 실행
tokens = enc.encode("안녕, 세상아!")
print(len(tokens))
print(tokens)

# 디코딩 실행
print(enc.decode(tokens))

# 분할된 상태로 디코딩
def data2str(data):
    try:
        return data.decode('utf-8')
    except UnicodeError:
        return data
print([data2str(data) for data in enc.decode_tokens_bytes(tokens)])
