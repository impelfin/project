import openai
import textwrap

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

resps = response_from_ChatAI("ChatGPT는 무엇인가요?", 2) # 두 개의 응답 설정

for resp in resps:
    shorten_resp = textwrap.shorten(resp, 100, placeholder=' [..이하 생략..]')
    print(shorten_resp) # 축약 내용 출력
    print() # 빈 줄 하나를 출력
