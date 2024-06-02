import openai

file_path = "./data/aws2024.m4a"
audio_file = open(file_path, "rb")

# 지정한 형식으로 음성 추출
response = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file,
            response_format="text" # text, srt, vtt, json, verbose_json 중 하나 선택
            )
audio_file.close()
# print(response[:100]) # 일부 출력
print(response) # 전체 출력
