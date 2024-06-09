from langchain.llms import OpenAI

# LLM 준비
llm = OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0.9
)

# LLM 호출
print(llm("컴퓨터 게임을 만드는 새로운 한국어 회사명을 하나 제안해 주세요"))

