import openai

# 비디오, 오디오 파일 열기
file_path = "./data/서연의_하루_TTS_배경음악_short.mp3"
audio_file = open(file_path, "rb")

# 지정한 형식으로 음성 추출
response = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file,
            response_format="text" # text, srt, vtt, json, verbose_json 중 하나 선택
            )
audio_file.close()
print(response[:100]) # 일부 출력
# print(response) # 전체 출력
