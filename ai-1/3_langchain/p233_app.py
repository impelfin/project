from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# 템플릿 생성
template = """{subject}를 주제로 {target}를 작성해 주세요."""

# 프롬프트 템플릿 생성
prompt = PromptTemplate(
    template=template,
    input_variables=["subject", "target"]
)

# LLMChain 생성
llm_chain = LLMChain(
    llm=OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0
    ),
    prompt=prompt,
    verbose=True
)

# LLMChain 실행
print(llm_chain.predict(subject="고양이", target="시"))

