from langchain.prompts import PromptTemplate

# jinja2를 이용한 프롬프트 템플릿 준비
jinja2_prompt = PromptTemplate(
    input_variables=["items"],
    template_format="jinja2",
    template="""
{% for item in items %}
Q: {{ item.question }}
A: {{ item.answer }}
{% endfor %}
"""
)

# 프롬프트 생성
items=[
    {"question": "foo", "answer": "bar"},
    {"question": "1", "answer": "2"}
]
print(jinja2_prompt.format(items=items))
