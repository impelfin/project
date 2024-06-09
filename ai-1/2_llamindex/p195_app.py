import os
from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, StorageContext, ServiceContext, LLMPredictor, LangchainEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import HuggingFaceEmbeddings
import faiss

# 문서 로드 (data 폴더에 문서를 넣어두세요)
documents = SimpleDirectoryReader("data").load_data()
print("Documents loaded successfully")

# 임베딩 모델 준비
embed_model = LangchainEmbedding(HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
))
print("Embedding model initialized successfully")

# LLMPredictor 준비
llm_predictor = LLMPredictor(llm=ChatOpenAI(
    temperature=0,  # 온도
    model_name="gpt-3.5-turbo"  # 모델명
))
print("LLMPredictor initialized successfully")

# faiss의 인덱스 생성
faiss_index = faiss.IndexFlatL2(384)  # 임베딩 벡터 차원에 맞게 조정
vector_store = FaissVectorStore(faiss_index=faiss_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
service_context = ServiceContext.from_defaults(embed_model=embed_model, llm_predictor=llm_predictor)
print("FAISS index and vector store initialized successfully")

# 인덱스 생성
index = GPTVectorStoreIndex.from_documents(
    documents, 
    storage_context=storage_context,
    service_context=service_context
)
print("Index created successfully")

# 쿼리 엔진 생성
query_engine = index.as_query_engine()
print("Query engine created successfully")

# 질의응답
response = query_engine.query("미코의 소꿉친구 이름은?")
print(response)

