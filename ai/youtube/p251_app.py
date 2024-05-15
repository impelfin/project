import openai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import textwrap

def get_video_id(video_url):
    video_id = video_url.split('v=')[1][:11]
    
    return video_id 

video_url = "https://www.youtube.com/watch?v=pSJrML-TTmI" # 동영상의 URL 입력
video_id = get_video_id(video_url)

transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])

text_formatter = TextFormatter() # SRT 형식으로 출력 지정
text_formatted = text_formatter.format_transcript(transcript)
text_info = text_formatted.replace("\n", " ") # 개행문자 제거

def answer_from_given_info(question_info, prompt):

    # 입력 정보에 기반해 답변 요청
    user_content = f"{prompt} 다음 내용을 바탕으로 질문에 답해 줘. {question_info}" 
    
    messages = [ {'role': 'user', 'content': user_content} ]

    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages,                        
                        max_tokens=500,
                        stop = ["."],
                        temperature=0.2 )
    
    return response['choices'][0]['message']['content'] # 응답 결과 반환

question_info = text_info # 자막을 가져온 내용을 학습 데이터로 사용
prompt = "허준이 교수가 받은 상은 무엇인가요?" # 질문
print(prompt)
response = answer_from_given_info(question_info, prompt)
print(response)

print('-' * 70)

question_info = text_info # 자막을 가져온 내용을 학습 데이터로 사용
prompt = "허준이 교수는 어느 대학 교수인가요?" # 질문
print(prompt)
response = answer_from_given_info(question_info, prompt)
print(response)
