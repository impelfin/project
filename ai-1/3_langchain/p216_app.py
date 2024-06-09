import langchain
from langchain.cache import InMemoryCache
from langchain.llms import OpenAI

# LLM 준비
llm = OpenAI(
    model="gpt-3.5-turbo-instruct",  # 모델 ID
    temperature=0  # 무작위성
)

# 캐시 활성화
langchain.llm_cache = InMemoryCache()

# 첫 번째 LLM 호출
print(llm.generate(["하늘의 색깔은?"]))

# 2번째 이후 LLM 호출
print(llm.generate(["하늘의 색깔은?"]))

