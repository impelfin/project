from llama_index import SimpleDirectoryReader
from llama_index import GPTVectorStoreIndex, ServiceContext, LLMPredictor
from langchain.chat_models import ChatOpenAI

# 문서 로드(data 폴더에 문서를 넣어 두세요)
documents = SimpleDirectoryReader("data").load_data()

# LLMPredictor 준비
llm_predictor = LLMPredictor(llm=ChatOpenAI(
    temperature=0, # 온도
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

# 쿼리 엔진 생성
query_engine = index.as_query_engine()

# 질의응답
print('-' * 50)
print(query_engine.query("미코의 소꿉친구 이름은?"))

# 질의응답
print('-' * 50)
print(query_engine.query("울프 코퍼레이션의 CEO의 이름은?"))

# 질의응답
print('-' * 50)
print(query_engine.query("미코의 성격은?"))
print('-' * 50)
