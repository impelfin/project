from langchain.chains import ConversationChain
from langchain.llms import OpenAI

# 대화 체인 생성
chain = ConversationChain(
    llm=OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0
    ),
    verbose=True
)

# 체인 실행
chain.run("우리집 반려견 이름은 보리입니다")

# 체인 실행
chain.predict(input="우리집 반려견 이름을 불러주세요")

