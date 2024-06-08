import deepl # deepl 라이브러리 임포트
import os

folder = "./data/"
input_path  = folder + "President_Obamas_Farewell_Address_영어_원본.pdf" # 원본 파일 경로
output_path = folder + "President_Obamas_Farewell_Address_한국어_번역.pdf" # 번역 파일 경로

auth_key = os.environ["DEEPL_AUTH_KEY"] # DeepL 인증 키
translator = deepl.Translator(auth_key) # translator 객체를 생성

# 문서 번역 실행
result = translator.translate_document_from_filepath( 
            input_path,       # 입력 문서(원본) 파일의 경로
            output_path,      # 출력 문서(번역) 파일의 경로
            target_lang="KO") # 대상(타깃) 문서의 언어 코드

print(result.done) # 문서 번역 결과 확인
