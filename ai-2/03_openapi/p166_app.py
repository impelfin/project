import openai

user_input = input("AI와 채팅할 내용을 입력하세요 (종료하려면 end를 입력하세요) \n[나] : ")

messages = [{"role": "system", "content": "You are a helpful assistant."}]   

ai_message = ""    
while(user_input !="end"):
    message = [{"role": "assistant", "content": ai_message},
               {"role": "user", "content": user_input}]
    messages.extend(message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=messages,
        max_tokens=1000,
        temperature=0.9,
        n=1)
    
    ai_message = response.choices[0].message['content']
    print(f"[AI]\n{ai_message}")
    user_input = input("\n[나] : ")

if(user_input =="end"):
    print("AI와 채팅을 종료합니다.")
