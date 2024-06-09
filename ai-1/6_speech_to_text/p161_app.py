import openai

# 음성 텍스트 변환(현재 폴더에 오디오 파일을 업로드해두세요)
audio_file= open("audio.mp3", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
print(transcript["text"])
