from llama_index import SimpleDirectoryReader
from llama_index import LLMPredictor, ServiceContext
from llama_index import GPTVectorStoreIndex
from langchain.chat_models import ChatOpenAI

# 문서 로드
documents = SimpleDirectoryReader("data").load_data()
print("documents :", documents)

# LLMPredictor 준비
llm_predictor = LLMPredictor(llm=ChatOpenAI(
    temperature=0,  # 온도
    model_name="gpt-3.5-turbo" # 모델명
))

# ServiceContext 준비
service_context = ServiceContext.from_defaults(
    llm_predictor=llm_predictor, 
)

# 인덱스 생성
index = GPTVectorStoreIndex.from_documents(
    documents, 
    service_context=service_context, 
)
