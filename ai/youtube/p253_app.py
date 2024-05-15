import yt_dlp
from pathlib import Path

# 유튜브 비디오 정보를 가져오는 함수
def get_youtube_video_info(video_url):
    ydl_opts = {
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_info = ydl.extract_info(video_url, download=False)
        video_id = video_info['id']
        title = video_info['title']
        upload_date = video_info['upload_date']
        channel = video_info['channel']
        duration = video_info['duration_string']

    return video_id, title, upload_date, channel, duration

# 파일 이름에 부적합한 문자를 제거하는 함수
def remove_invalid_char_for_filename(input_str):
    invalid_characters = '<>:"/\|?*'
    for char in invalid_characters:
        input_str = input_str.replace(char, '_')
    input_str = input_str.rstrip('.')  # 마지막 '.' 제거를 더 간결하게 처리
    return input_str

# 유튜브 비디오를 오디오 파일로 다운로드하는 함수 
def download_youtube_as_mp3(video_url, folder, file_name=None):
    _, title, _, _, _ = get_youtube_video_info(video_url)
    filename_no_ext = remove_invalid_char_for_filename(title)
    
    if file_name is None:
        download_file = f"{filename_no_ext}.mp3"
    else:
        download_file = file_name

    outtmpl_str = Path(folder) / download_file  # 파일 경로 구성을 Path로 처리
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(outtmpl_str),
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'extract_audio': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return title, outtmpl_str
    except Exception as e:
        return str(e), None

video_url = "https://www.youtube.com/watch?v=EKqQvzyVAh4"
download_folder = "./data"
file_name = "youtube_video_KBS_news.mp3"

title, download_path = download_youtube_as_mp3(video_url, download_folder, file_name)

if download_path:
    print("- 유튜브 제목:", title)
    print("- 다운로드한 파일명:", download_path.name)
else:
    print("Error downloading video:", title)
