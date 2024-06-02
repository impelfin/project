import openai
from pathlib import Path
import os

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

audio_file = "./data/youtube_video_file.mp3"

print(f"[음성 파일 경로] {audio_file}\n")
r_format = "srt" # 출력 형식을 srt로 지정

transcript, output_path = audio_transcribe(audio_file, r_format)    

print(f"- [텍스트 추출 형식] {r_format}")
print(f"- [출력 파일] {output_path.name}")
print(f"- [음성 추출 결과(일부 출력)]\n{transcript[:137]}") # 추출 결과 출력(일부)
# print(f"- [음성 추출 결과]\n{transcript}") # 추출 결과 출력(전체)
