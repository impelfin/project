from langchain.agents import load_tools
from langchain.llms import OpenAI
from langchain.agents import initialize_agent
import os

# Serpapi API 키 설정
serpapi_api_key = os.environ.get('SERPAPI_API_KEY')

# 도구 준비
tools = load_tools(
    tool_names=["serpapi", "llm-math"], 
    llm=OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0
    ),
    serpapi_api_key = serpapi_api_key
)

# 에이전트 생성
agent = initialize_agent(
    agent="zero-shot-react-description",
    llm=OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0
    ),
    tools=tools,
    verbose=True
)

# 에이전트 실행
agent.run("123*4를 계산기로 계산하세요")
print('-' * 50)

# 에이전트 실행
agent.run("오늘 한국 서울의 날씨를 웹 검색으로 확인하세요")


