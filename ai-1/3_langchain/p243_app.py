from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.chains import RetrievalQAWithSourcesChain
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

# 메타데이터 준비
metadatas=[
    {"source": "1장"},
    {"source": "2장"},
    {"source": "3장"},
    {"source": "4장"},
    {"source": "5~6장"},
    {"source": "7장"}
]

# 벡터 데이터베이스 생성
docsearch = FAISS.from_texts(
    texts=texts, # 청크 배열
    embedding=OpenAIEmbeddings(), # 임베딩
    metadatas=metadatas # 메타데이터
)

# 소스가 있는 질의응답 체인 생성
qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
    llm=OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0
    ),
    chain_type="stuff",
    retriever=docsearch.as_retriever(),
)

# 소스가 있는 질의응답 체인 실행
print(qa_chain({"question": "미코의 소꿉친구 이름은?"}))

