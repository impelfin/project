from langchain.agents import load_tools
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.agents import initialize_agent

# 도구 준비
tools = load_tools(
    tool_names=["serpapi", "llm-math"], # 도구 이름
    llm=ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0
    ) # 도구의 초기화에 사용할 LLM
)

# 메모리 생성
memory = ConversationBufferMemory(
    memory_key="chat_history", 
    return_messages=True
)

# 에이전트 생성
agent = initialize_agent(
    agent="chat-conversational-react-description", # 에이전트 유형 설정
    llm=ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0
    ), # 에이전트 초기화에 사용할 LLM
    tools=tools, # 도구
    memory=memory, # 메모리
    verbose=True # 상세 정보 출력
)

# 에이전트 실행
print(agent.run("좋은 아침입니다."))
print('-' * 50)

# 에이전트 실행
print(agent.run("우리집 반려견 이름은 보리입니다."))
print('-' * 50)

# 에이전트 실행
print(agent.run("우리집 반려견 이름을 불러주세요."))
print('-' * 50)

# 에이전트 실행
print(agent.run("123*4를 계산기로 계산해 주세요"))
print('-' * 50)

# 에이전트 실행
print(agent.run("오늘 서울의 날씨를 웹에서 검색해 주세요."))
print('-' * 50)


