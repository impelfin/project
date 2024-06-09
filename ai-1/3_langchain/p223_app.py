from langchain.prompts import PromptTemplate

# 하나의 입력 변수가 있는 프롬프트 템플릿 만들기
one_input_prompt = PromptTemplate(
    input_variables=["content"],
    template="멋진 {content}이라고 하면?"
)

# 프롬프트 생성
print(one_input_prompt.format(content="동물"))

