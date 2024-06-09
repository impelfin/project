from llama_index import download_loader
from llama_index import GPTVectorStoreIndex

# 문서 로드
BeautifulSoupWebReader = download_loader("BeautifulSoupWebReader")
loader = BeautifulSoupWebReader()
documents = loader.load_data(urls=["https://openai.com/blog/planning-for-agi-and-beyond"])

# 인덱스 생성
index = GPTVectorStoreIndex.from_documents(documents)

# 쿼리 엔진 생성
query_engine = index.as_query_engine()

# 질의응답
print(query_engine.query("이 웹페이지에서 전하고 싶은 말은 무엇인가요? 한국어로 대답해 주세요."))
