import os
from langchain.agents import load_tools
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI

# WOLFRAM_ALPHA_APPID 키 설정
wolfram_alpha_appid = os.environ.get('WOLFRAM_ALPHA_APPID')

# 도구 준비
tools = load_tools(["wolfram-alpha"])

# 메모리 생성
memory = ConversationBufferMemory(
    memory_key="chat_history", 
    return_messages=True
)

# 에이전트 생성
agent = initialize_agent(
    agent="zero-shot-react-description",
    llm=ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0
    ), 
    tools=tools,
    memory=memory,
    verbose=True
)

# 에이전트 실행
print("How many kilometers is the distance from Seoul to Busan?")
print(agent.run("How many kilometers is the distance from Seoul to Busan?"))