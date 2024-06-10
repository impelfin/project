from langchain.memory import ConversationSummaryMemory
from langchain.chat_models import ChatOpenAI

# 메모리 생성
memory = ConversationSummaryMemory(
    llm=ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0
    ),
    return_messages=True
)
memory.save_context({"input": "배고파"}, {"ouput": "어디 가서 밥 먹을까?"})
memory.save_context({"input": "라면 먹으러 가자"}, {"ouput": "역 앞에 있는 분식집으로 가자"})
memory.save_context({"input": "그럼 출발!"}, {"ouput": "OK!"})

# 메모리 변수 가져오기
print(memory.load_memory_variables({}))
