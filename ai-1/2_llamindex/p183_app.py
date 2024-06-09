from llama_index import GPTVectorStoreIndex, PromptHelper, ServiceContext
from llama_index import SimpleDirectoryReader

# 문서 로드
documents = SimpleDirectoryReader("data").load_data()
print("documents :", documents)

# PromptHelper 준비
prompt_helper=PromptHelper(
    max_input_size=4096, # LLM 입력의 최대 토큰 수
    num_output=256, # LLM 출력의 토큰 수
    max_chunk_overlap=20, # 청크 오버랩의 최대 토큰 개수
)

# ServiceContext 준비
service_context = ServiceContext.from_defaults(
    prompt_helper=prompt_helper
)

# 인덱스 생성
index = GPTVectorStoreIndex.from_documents(
    documents, # 문서
    service_context=service_context, # ServiceContext
)
