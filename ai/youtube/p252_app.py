import yt_dlp
import openai
from pathlib import Path
import textwrap
import os
import deepl

## Part 1
#
# 유튜브 비디오 정보를 가져오는 함수
def get_youtube_video_info(video_url):
    ydl_opts = {
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(video_url, download=False)
        video_id = video_info['id']
        title = video_info['title']
        upload_date = video_info['upload_date']
        channel = video_info['channel']
        duration = video_info['duration_string']

    return video_id, title, upload_date, channel, duration

# 파일 이름에 부적합한 문자를 제거하는 함수
def remove_invalid_char_for_filename(input_str):
    invalid_characters = '<>:"/\|?*'
    for char in invalid_characters:
        input_str = input_str.replace(char, '_')
    input_str = input_str.rstrip('.')  # 마지막 '.' 제거를 더 간결하게 처리
    return input_str

# 유튜브 비디오를 오디오 파일로 다운로드하는 함수 
def download_youtube_as_mp3(video_url, folder, file_name=None):
    _, title, _, _, _ = get_youtube_video_info(video_url)
    filename_no_ext = remove_invalid_char_for_filename(title)
    
    if file_name is None:
        download_file = f"{filename_no_ext}.mp3"
    else:
        download_file = file_name

    outtmpl_str = Path(folder) / download_file  # 파일 경로 구성을 Path로 처리
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(outtmpl_str),
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'extract_audio': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return title, outtmpl_str
    except Exception as e:
        return str(e), None

video_url = "https://www.youtube.com/watch?v=EKqQvzyVAh4"
download_folder = "./data"
file_name = "youtube_video_KBS_news.mp3"

title, download_path = download_youtube_as_mp3(video_url, download_folder, file_name)

if download_path:
    print("- 유튜브 제목:", title)
    print("- 다운로드한 파일명:", download_path.name)
else:
    print("Error downloading video:", title)

print('-' * 70)

## Part 2 
#
# Audio 자막을 Text로 변환. 다중언어인 경우 영어로 출력
def audio_transcribe(input_path, resp_format= "text", lang="en"):  
    
    openai.api_key = os.environ["OPENAI_API_KEY"] # OpenAI API Key
    with open(input_path, "rb") as f: # 음성 파일 열기
        # 음성 추출  
        transcript = openai.Audio.transcribe(
            model="whisper-1",
            file=f,
            language=lang,            
            response_format=resp_format # 추출할 텍스트 형식 지정
        )
    # 음성을 텍스트로 추출한 후에 텍스트 파일로 저장
    path = Path(input_path)
    if resp_format == "text":
        output_file = f"{path.parent}/{path.stem}.txt"
    else:
        output_file = f"{path.parent}/{path.stem}.srt"
        
    output_path = Path(output_file)    
        
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(transcript)

    return transcript, output_path

audio_path = download_path
   
print(f"[오디오 파일명] {audio_path.name}\n")
r_format = "text" # 출력 형식을 text로 지정

transcript, output_file = audio_transcribe(audio_path, r_format)
shorten_text = textwrap.shorten(transcript, 250, placeholder=' [..이하 생략..]')

print(f"- [텍스트 추출 형식] {r_format}")
print(f"- [출력 파일] {output_file.name}")
print(f"- [음성 추출 결과]\n{shorten_text}" )

print('-' * 70)

## Part 3
#
# 영어 자막을 한국어 자막으로 번역
def transplate_text_file(input_path, t_lang="KO"):
    
    # 원본 파일 읽기
    with open(input_path, encoding='utf-8') as f:
        text = f.read()

    # 번역 수행
    auth_key = os.environ["DEEPL_AUTH_KEY"] # Deepl 인증 키
    translator = deepl.Translator(auth_key) # translator 객체를 생성
    result = translator.translate_text(text, target_lang=t_lang)
    
    # 번역 파일 쓰기
    path = Path(input_path)
    output_file = f"{path.parent}/{path.stem}_번역_{t_lang}{path.suffix}"
    
    output_path = Path(output_file)    

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result.text)   

    return output_path

input_file = output_file
translated_file = transplate_text_file(input_file)

print("- 번역 파일:", translated_file.name)

## Part 4
#
# 한국어 자막으로 학습하여 질문에 답변
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

file_name = translated_file # 유튜브 내용을 학습 데이터로 사용
with open(file_name, encoding='utf-8') as f: # 텍스트 파일 읽기
    text = f.read() # 텍스트 파일 내용

print('-' * 70)

question_info = text # 질문에 대한 학습 데이터
prompt = "마이크로소프트는 OpenAI 개발에 얼마를 투자했나요?" # 질문

response = answer_from_given_info(question_info, prompt)
print(response)

print('-' * 70)

prompt = "KSB가 인터뷰한 사람은 누구인가요?"
response = answer_from_given_info(question_info, prompt)
print(response)
