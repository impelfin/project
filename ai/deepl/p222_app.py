import deepl # deepl 라이브러리를 임포트
import os

auth_key = os.environ["DEEPL_AUTH_KEY"] # DeepL 인증 키
translator = deepl.Translator(auth_key) # translator 객체를 생성

text = "Improve your writing in just one click." # 번역할 원본 텍스트(영어)
result = translator.translate_text( # 번역 결과 객체를 result 변수에 할당
                text,               # 원본(소스) 텍스트
                target_lang="KO")   # 대상(타깃) 언어 코드 

print("- 감지된 언어 코드:", result.detected_source_lang)
print("- 번역 결과:", result.text)
