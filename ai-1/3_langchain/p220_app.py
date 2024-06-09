import asyncio
import time
from langchain.llms import OpenAI

# 이벤트 루프를 중첩하는 설정
import nest_asyncio

nest_asyncio.apply()

# 비동기 처리로 한 번만 호출하는 함수
async def async_generate(llm):
    resp = await llm.agenerate(["안녕하세요!"])
    print(resp.generations[0][0].text)

# 비동기 처리로 10회 호출하는 함수
async def generate_concurrently():
    llm = OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0.9
    )
    tasks = [async_generate(llm) for _ in range(10)]
    await asyncio.gather(*tasks)

# 시간 측정 시작
s = time.perf_counter()

# 비동기 처리로 10회 호출
asyncio.run(generate_concurrently())

# 시간 측정 완료
elapsed = time.perf_counter() - s
print(f"{elapsed:0.2f} 초")