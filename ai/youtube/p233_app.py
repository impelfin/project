import yt_dlp
from pathlib import Path

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

# 파일 이름에 부적합한 문자를 제거하는 함수
def remove_invalid_char_for_filename(input_str):
    # 윈도우 파일 이름에 안 쓰는 문자 제거 
    invalid_characters = '<>:"/\|?*'
    
    for char in invalid_characters:
        input_str = input_str.replace(char, '_')
        
    # 파일명 마지막에 . 제거
    while input_str.endswith('.'):
        input_str = input_str[:-1]  
        
    return input_str

# 유튜브 비디오를 오디오 파일로 다운로드하는 함수 
def download_youtube_as_mp3(video_url, folder, file_name=None):
    
    _, title, _, _, _ = get_youtube_video_info(video_url)
    filename_no_ext = remove_invalid_char_for_filename(title)
        
    if file_name == None:
        download_file = f"{filename_no_ext}.mp3"
    else:
        download_file = file_name

    outtmpl_str = f'{folder}/{download_file}'
    download_path = Path(outtmpl_str)  
        
    ydl_opts = {     
        'extract_audio': True,      # 다양한 옵션 지정                    
        'format': 'bestaudio', # 다운로드 형식 지정 (최적)
        'outtmpl': outtmpl_str,     # 다운로드 경로 지정
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(video_url, download=False) # 비디오 정보 추출
        title = video_info.get('title', None) # 비디오 정보 중 제목만 추출
        ydl.download(video_url) # 다운로드

    return title, download_path

video_url = 'https://www.youtube.com/watch?v=Ks-_Mh1QhMc'
download_folder = "./data" # 다운로드할 폴더는 미리 생성 후 지정
file_name = "youtube_video_file.mp3"        # 오디오 파일 이름 지정
title, download_path = download_youtube_as_mp3(video_url, download_folder, file_name)
# title, download_path = download_youtube_as_mp3(video_url, download_folder)

print("- 유튜브 제목:", title)
print("- 다운로드한 파일명:", download_path.name)
