import openai

# 음성을 영어로 번역하고 텍스트로 변환(현재 폴더에 오디오 파일을 업로드해둡니다)
audio_file= open("audio.mp3", "rb")
transcript = openai.Audio.translate("whisper-1", audio_file)
print(transcript["text"])
