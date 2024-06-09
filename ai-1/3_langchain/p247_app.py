from langchain.chains import PALChain
from langchain import OpenAI

# PALChain 생성
pal_chain = PALChain.from_math_prompt(
    llm=OpenAI(
        model="gpt-3.5-turbo-instruct",
    ), 
    verbose=True
)

# PALChain 실행
question = "제인은 앨리스가 키우는 반려동물의 3배가 되는 반려동물을 키우고 있다. 앨리스가 2마리의 반려동물을 키우고 있다면 두 사람이 키우고 있는 반려동물의 총 마리 수는?"
print(pal_chain.run(question))

