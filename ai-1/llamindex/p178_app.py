from llama_index import SimpleDirectoryReader

# 문서 로드
documents = SimpleDirectoryReader("data").load_data()
print("documents :", documents)

