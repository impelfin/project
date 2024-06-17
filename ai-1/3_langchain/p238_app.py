from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain

## 첫 번째 체인

# 템플릿 생성
template = """당신은 극작가입니다. 극의 제목과 시대적 배경이 주어졌을 때, 그 줄거리를 작성하는 것이 당신의 임무입니다.

제목:{title}
시대:{era}
시놉시스:"""

# 프롬프트 템플릿 생성
prompt = PromptTemplate(
    input_variables=["title", "era"], 
    template=template
)

# LLMChain 생성
chain1 = LLMChain(
    llm=OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0
    ),
    prompt=prompt, 
    output_key="synopsis"
)

## 두 번째 체인

# 템플릿 생성
template = """당신은 연극 평론가입니다. 연극의 시놉시스가 주어지면 그 리뷰를 작성하는 것이 당신의 임무입니다.

시놉시스:
{synopsis}
리뷰:"""

# 프롬프트 템플릿 생성
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
    prompt=prompt, 
    output_key="review"
)

## SequentialChain으로 두 개의 체인 연결하기


# SequentialChain으로 두 개의 체인을 연결
overall_chain = SequentialChain(
    chains=[chain1, chain2],
    input_variables=["title", "era"],
    output_variables=["synopsis", "review"],
    verbose=True
)

# SequentialChain 실행
print(overall_chain({"title":"서울 랩소디", "era": "100년 후의 미래"}))

