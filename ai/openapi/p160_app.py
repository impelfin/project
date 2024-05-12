import openai

# 대화 메시지 정의
messages = [
    {"role": "user", "content": "대한민국의 수도는 어디인가요?"}
]

# Chat Completions API 호출
response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", # 모든 사용자 설정 가능
                # model="gpt-3.5-turbo-16k", # gpt-3.5-turbo 대비 4배 긴 토큰 처리
                # model="gpt-4", # GPT-4 모델 사용
                messages=messages, # 전달할 메시지 지정
                max_tokens=1000, # 응답 최대 토큰 수 지정
                temperature=0.8, # 완성의 다양성을 조절하는 온도 설정
                n=1 # 생성할 완성의 개수 지정
)

# 응답 출력
assistant_reply = response.choices[0].message['content'] # 첫 번째 응답 결과 가져오기
print(assistant_reply)
