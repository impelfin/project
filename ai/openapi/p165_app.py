import openai

def response_from_ChatAI(user_content, r_num=1):
    
    # 대화 메시지 정의
    messages = [ {"role": "user", "content": user_content} ]

    # Chat Completions API 호출
    response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=1000,
                    temperature=0.8,
                    n=r_num 
    )
    
    # 응답을 리스트에 할당
    assistant_replies = []
    
    for choice in response.choices:
        assistant_replies.append(choice.message['content'])
        
    return assistant_replies # 응답 반환

resps = response_from_ChatAI("두 숫자를 입력받아 더하는 파이썬 함수 만들어 줘")
print(resps[0])
