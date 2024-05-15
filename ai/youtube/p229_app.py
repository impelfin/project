import yt_dlp

# 유튜브 비디오 정보를 가져오는 함수
def get_youtube_video_info(video_url):
    ydl_opts = {            # 다양한 옵션 지정
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(video_url, download=False) # 비디오 정보 추출
        video_id = video_info['id']              # 비디오 정보에서 비디오 ID 추출
        title = video_info['title']              # 비디오 정보에서 제목 추출
        upload_date = video_info['upload_date']  # 비디오 정보에서 업로드 날짜 추출
        channel = video_info['channel']          # 비디오 정보에서 채널 이름 추출
        duration = video_info['duration_string']

    return video_id, title, upload_date, channel, duration

video_url = 'https://www.youtube.com/watch?v=pSJrML-TTmI'
print(get_youtube_video_info(video_url))
