from langchain.prompts import PromptTemplate

# 여러 개의 입력 변수가 있는 프롬프트 템플릿 만들기
multiple_input_prompt = PromptTemplate(
    input_variables=["adjective", "content"],
    template="{adjective}{content}이라고 하면?"
)

# 프롬프트 생성
print(multiple_input_prompt.format(adjective="멋진", content="동물"))
