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

shorten_text_info = textwrap.shorten(text_info, 150 ,placeholder=' [..이하 생략..]')
print(shorten_text_info) # 축약 출력
# print(text_info) # 전체 내용 출력
