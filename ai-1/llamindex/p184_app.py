import os
from langchain.embeddings import HuggingFaceEmbeddings
from llama_index import GPTVectorStoreIndex, ServiceContext, LangchainEmbedding, LLMPredictor
from llama_index import SimpleDirectoryReader
from langchain.chat_models import ChatOpenAI


# 문서 로드
documents = SimpleDirectoryReader("data").load_data()
# print("documents:", documents)

# 임베딩 모델 준비
embed_model = LangchainEmbedding(HuggingFaceEmbeddings(
    model_name="bongsoo/moco-sentencedistilbertV2.1"
))
print("Embedding model initialized successfully")

# LLMPredictor 준비
llm_predictor = LLMPredictor(llm=ChatOpenAI(
    temperature=0,  # 온도
    model_name="gpt-3.5-turbo"  # 모델명
))
print("LLMPredictor initialized successfully")

# ServiceContext 준비
service_context = ServiceContext.from_defaults(
    embed_model=embed_model,
    llm_predictor=llm_predictor
)
print("ServiceContext created successfully")

# 인덱스 생성
index = GPTVectorStoreIndex.from_documents(
    documents,  # 문서
    service_context=service_context  # ServiceContext
)
print("Index created successfully")

# 쿼리 엔진 생성
query_engine = index.as_query_engine()
print("Query engine created successfully")

# 질의응답
response = query_engine.query("미코의 소꿉친구 이름은?")
print(response)

# 응답 출력
print("response:", response.response, "\n")

# 소스 출력
print("source_nodes:", response.source_nodes, "\n")

