from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain

## 첫 번째 체인

# 템플릿 준비
template = """당신은 극작가입니다. 연극 제목이 주어졌을 때, 그 줄거리를 작성하는 것이 당신의 임무입니다.

제목:{title}
시놉시스:"""

# 프롬프트 템플릿 준비
prompt = PromptTemplate(
    input_variables=["title"],
    template=template
)

# LLMChain 준비
chain1 = LLMChain(
    llm=OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0
    ),
    prompt=prompt
)


## 두 번째 체인

# 템플릿 생성
template = """당신은 연극 평론가입니다. 연극의 시놉시스가 주어지면 그 리뷰를 작성하는 것이 당신의 임무입니다.

시놉시스:
{synopsis}
리뷰:"""

# 프롬프트 템플릿 준비
prompt = PromptTemplate(
    input_variables=["synopsis"],
    template=template
)

# LLMChain 준비
chain2 = LLMChain(
    llm=OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0
    ),
    prompt=prompt
)


## SimpleSequentialChain으로 두 개의 체인 연결하기

# SimpleSequentialChain으로 두 개의 체인을 연결
overall_chain = SimpleSequentialChain(
    chains=[chain1, chain2],
    verbose=True
)

# SimpleSequentialChain 실행
print(overall_chain.run("서울 랩소디"))
