from langchain.chains import OpenAIModerationChain
from langchain.chains import OpenAIModerationChain

# OpenAIModerationChain 준비
chain = OpenAIModerationChain()

# 문제없는 발언
text = "This is OK!"
print('User : ' + text)
print('Result : ' + chain.run(text))
print('-' * 50)

# 문제 발언
text = "I'll kill you!"
print('User : ' + text)
print('Result : ' + chain.run(text))
print('-' * 50)

# OpenAIModerationChain 준비
chain = OpenAIModerationChain(error=True)

try:
    # 문제 있는 발언
    text = "I'll kill you!"
    print('User : ' + text)
    print('Result : ' + chain.run(text))
    print('-' * 50)
except ValueError as e:
    print("문제 발언입니다!")
    print(e)

