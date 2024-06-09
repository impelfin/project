from langchain.llms import OpenAI

# LLM 준비
llm = OpenAI(
    model="gpt-3.5-turbo-instruct",  # 모델 ID
    temperature=0  # 무작위성
)

# LLM 호출
result = llm("고양이 울음소리는?")
print(result)

# 고급 LLM 호출
result = llm.generate(["고양이 울음소리는?", "까마귀 울음소리는?"])

# 출력 텍스트
print("response0:", result.generations[0][0].text)
print("response1:", result.generations[1][0].text)

# 사용한 토큰 개수
print("llm_output:", result.llm_output)

