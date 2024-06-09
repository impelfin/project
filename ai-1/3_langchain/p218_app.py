import langchain
from langchain.llms import OpenAI

# LLM 준비
llm = OpenAI(
    model="gpt-3.5-turbo-instruct",  # 모델 ID
    temperature=0  # 무작위성
)

# 캐시 비활성화
langchain.llm_cache = None

# LLM 호출
print(llm.generate(["하늘의 색깔은?"]))
