from langchain.memory import ConversationSummaryBufferMemory
from langchain.chat_models import ChatOpenAI

# 메모리 생성
memory = ConversationSummaryBufferMemory(
    llm=ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0
    ), 
    max_token_limit=50, 
    return_messages=True
)
memory.save_context({"input": "안녕"}, {"ouput": "무슨 일이야?"})
memory.save_context({"input": "배고파"}, {"ouput": "나도"})
memory.save_context({"input": "밥 먹자"}, {"ouput": "OK!"})

# 메모리 변수 가져오기
print(memory.load_memory_variables({}))

