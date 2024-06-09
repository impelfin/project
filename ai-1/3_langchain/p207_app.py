from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# 프롬프트 템플릿 만들기
prompt = PromptTemplate(
    input_variables=["product"],
    template="{product}을 만드는 새로운 한국어 회사명을 하나 제안해 주세요",
)

# 체인 생성
chain = LLMChain(
    llm=OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0.9
    ),
    prompt=prompt
)

# 체인 실행
print(chain.run("가정용 로봇"))
