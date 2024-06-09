from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.llms import OpenAI

# 문서 로드
with open("akazukin_all.txt") as f:
    test_all = f.read()

# 청크 분할
text_splitter = CharacterTextSplitter(
    separator = "\n\n", # 구분 기호
    chunk_size=300, # 청크의 최대 문자 수
    chunk_overlap=20, # 최대 오버랩 문자 수
)
texts = text_splitter.split_text(test_all)

# 확인
print(len(texts))
for text in texts:
    print(text[:10], ":", len(text))

# 청크 배열을 문서 배열로 변환
docs = [Document(page_content=t) for t in texts]

# 요약 체인 생성
chain = load_summarize_chain(
    llm=OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0
    ),
    chain_type="map_reduce",
)

# 요약 체인 실행
print(chain.run(docs))

