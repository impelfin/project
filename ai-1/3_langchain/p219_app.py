import time
from langchain.llms import OpenAI

# 동기화 처리로 10번 호출하는 함수
def generate_serially():
    llm = OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0.9
    )
    for _ in range(10):
        resp = llm.generate(["안녕하세요!"])
        print(resp.generations[0][0].text)


# 시간 측정 시작
s = time.perf_counter()

# 동기화 처리로 10번 호출
generate_serially()

# 시간 측정 완료
elapsed = time.perf_counter() - s
print(f"{elapsed:0.2f} 초")
