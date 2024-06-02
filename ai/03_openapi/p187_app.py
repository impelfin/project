import openai

file_path = "./data/서연의_하루_TTS_배경음악_short.mp3"
audio_file = open(file_path, "rb")

# 지정한 형식으로 음성 추출 후 영어번역
response = openai.Audio.translate(
            model="whisper-1",
            file=open(file_path, "rb"),
            response_format="text" # text, srt, vtt, json, verbose_json 중 하나 선택
            )
audio_file.close()
print(response[:100]) # 일부 출력
# print(response) # 전체 출력