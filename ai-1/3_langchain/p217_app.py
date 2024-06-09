from langchain.llms import OpenAI

# LLM 준비
llm = OpenAI(
    model="gpt-3.5-turbo-instruct",  # 모델 ID
    temperature=0  # 무작위성
)

# 특정 LLM에 대한 메모리 캐시 비활성화
llm = OpenAI(
    model="gpt-3.5-turbo-instruct",
    cache=False
)

# LLM 호출
print(llm.generate(["하늘의 색깔은?"]))
