from langchain.llms import OpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# 스트리밍 방식으로 출력할 LLM을 준비
llm = OpenAI(
    model="gpt-3.5-turbo-instruct",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
    verbose=True,
    temperature=0
)

# LLM 호출
resp = llm("즐거운 ChatGPT 생활을 가사로 만들어 주세요.")
