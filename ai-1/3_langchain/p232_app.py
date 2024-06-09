from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# 템플릿 생성
template = """Q: {question}
A:"""

# 프롬프트 템플릿 생성
prompt = PromptTemplate(
    input_variables=["question"],
    template=template
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
question = "기타를 잘 치는 방법은?"
print(llm_chain.predict(question=question))
