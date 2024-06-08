import deepl # deepl 라이브러리를 임포트
import os

auth_key = os.environ["DEEPL_AUTH_KEY"] # DeepL 인증 키
translator = deepl.Translator(auth_key) # translator 객체를 생성

text = "But" # 원본(소스) 텍스트

# 원본 텍스트의 언어(source_lang)를 미지정. 자동으로 감지함
result = translator.translate_text(
                text,              # 원본(소스) 텍스트
                target_lang="KO")  # 대상(타깃) 언어 코드 

print("- 감지된 언어 코드:", result.detected_source_lang)
print("- 번역 결과:", result.text)
