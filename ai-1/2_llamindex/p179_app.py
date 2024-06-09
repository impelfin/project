from llama_index import Document
from llama_index import GPTVectorStoreIndex

# 수동으로 문서 생성
texts = ["text1", "text2", "text3"]
documents = [Document(t) for t in texts]
print("documents :", documents)

# 인덱스 생성
index = GPTVectorStoreIndex.from_documents(documents)
