import deepl
from pathlib import Path
import os 

def transplate_text_file(input_path, t_lang="KO"):
    
    # 원본 파일 읽기
    with open(input_path, encoding='utf-8') as f:
        text = f.read()

    # 번역 수행
    auth_key = os.environ["DEEPL_AUTH_KEY"] # Deepl 인증 키
    translator = deepl.Translator(auth_key) # translator 객체를 생성
    result = translator.translate_text(text, target_lang=t_lang)
    
    # 번역 파일 쓰기
    path = Path(input_path)
    output_file = f"{path.parent}/{path.stem}_번역_{t_lang}{path.suffix}"
    
    output_path = Path(output_file)    

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result.text)   

    return output_path

input_file = "./data/youtube_video_file.srt"

translated_file = transplate_text_file(input_file)
print("- 번역 파일:", translated_file.name)
