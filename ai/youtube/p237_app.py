from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter, TextFormatter

def get_video_id(video_url):
    video_id = video_url.split('v=')[1][:11]
    
    return video_id 

video_url = 'https://www.youtube.com/watch?v=Ks-_Mh1QhMc'
video_id = get_video_id(video_url)

transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

print(f"- 유튜브 비디오 ID: {video_id}")
for transcript in transcript_list:
    print(f"- [자막 언어] {transcript.language}, [자막 언어 코드] {transcript.language_code}")

print('-' * 70)

transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
print(transcript[0:3])

print('-' * 70)

srt_formatter = SRTFormatter() # SRT 형식으로 출력 지정
srt_formatted = srt_formatter.format_transcript(transcript)
print(srt_formatted[:150])

print('-' * 70)

text_formatter = TextFormatter() # 텍스트(txt) 형식으로 출력 지정
text_formatted = text_formatter.format_transcript(transcript)
print(text_formatted[:100])

print('-' * 70)

download_folder = "./data" # 다운로드 폴더

# SRT 형식으로 파일 저장
srt_file = f"{download_folder}/{video_id}.srt"
print("- SRT 형식의 파일 경로:", srt_file)
with open(srt_file, 'w') as f:
    f.write(srt_formatted)
    
# 텍스트 형식으로 파일 저장    
text_file = f"{download_folder}/{video_id}.txt"
with open(text_file, 'w') as f:
    f.write(text_formatted)
print("- Text 형식의 파일 경로:", text_file)
