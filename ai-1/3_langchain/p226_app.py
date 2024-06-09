from langchain.prompts import FewShotPromptTemplate
from langchain.prompts import PromptTemplate

# 답변 예시 준비
examples = [
    {"input": "明るい", "output": "暗い"},
    {"input": "おもしろい", "output": "つまらない"},
]

# 프롬프트 템플릿 생성
example_prompt = PromptTemplate(
    input_variables=["input","output"],
    template="入力: {input}\n出力: {output}",
)

# 답변 예시를 포함한 프롬프트 템플릿 만들기
prompt_from_string_examples = FewShotPromptTemplate(
    examples=examples, # 답변 예시
    example_prompt=example_prompt, # 프롬프트 템플릿
    prefix="모든 입력에 대한 반의어를 입력하세요", # 접두사
    suffix="입력: {adjective}\n출력:", # 접미사
    input_variables=["adjective"], # 입력 변수
    example_separator="\n\n" # 구분 기호

)

# 프롬프트 생성
print(prompt_from_string_examples.format(adjective="큰"))

