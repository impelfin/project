from langchain.prompts import PromptTemplate

# 입력 변수가 없는 프롬프트 템플릿 만들기
no_input_prompt = PromptTemplate(
    input_variables=[],
    template="멋진 동물이라고 하면?"
)

# 프롬프트 생성
print(no_input_prompt.format())
