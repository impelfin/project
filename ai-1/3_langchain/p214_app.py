from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

# LLM 준비
chat_llm = ChatOpenAI(
    model="gpt-3.5-turbo",  # 모델 ID
    temperature=0  # 무작위성
)

# LLM 호출
messages = [
    HumanMessage(content="고양이 울음소리는?")
]
result = chat_llm(messages)
print(result)

# 고급 LLM 호출
messages_list = [
    [HumanMessage(content="고양이 울음소리는?")],
    [HumanMessage(content="까마귀 울음소리는?")]
]
result = chat_llm.generate(messages_list)

# 출력 텍스트
print("response0:", result.generations[0][0].text)
print("response1:", result.generations[1][0].text)

# 사용한 토큰 개수
print("llm_output:", result.llm_output)

