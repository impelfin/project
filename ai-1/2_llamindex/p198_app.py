import os
import pinecone
from pinecone import Pinecone, ServerlessSpec
from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, StorageContext, LLMPredictor, ServiceContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from langchain.chat_models import ChatOpenAI

# Pinecone API 키 설정
api_key = os.environ.get('PINECONE_API_KEY')

if api_key is None:
    raise ValueError("Pinecone API key is not set. Please set the environment variable 'PINECONE_API_KEY'.")

# Pinecone 초기화
pinecone = Pinecone(api_key=api_key)

# 문서 로드(data 폴더에 문서를 넣어두세요)
documents = SimpleDirectoryReader("data").load_data()

# 인덱스 이름 설정
index_name = "quickstart"

# 기존 인덱스 사용 또는 새 인덱스 생성
if index_name not in pinecone.list_indexes().names():
    pinecone.create_index(
        name=index_name,
        dimension=1536, # Replace with your model dimensions
        metric="euclidean", # Replace with your model metric
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ) 
    )

# Pinecone 인덱스 로드
pinecone_index = pinecone.Index(index_name)

# LLMPredictor 준비
llm_predictor = LLMPredictor(llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0))

# ServiceContext 준비
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

# 인덱스 생성
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = GPTVectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    service_context=service_context
)

# 쿼리 엔진 생성
query_engine = index.as_query_engine()

# 질의응답
response = query_engine.query("미코의 소꿉친구 이름은?")
print(response)
