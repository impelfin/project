from pathlib import Path

# 디렉터리 경로를 입력해 path 객체를 생성
dir_path = Path('./data') # 내려받을 폴더 생성   

# 디렉터리가 없다면 생성
dir_path.mkdir(parents=True, exist_ok=True)

# 생성한 디렉터리의 존재 여부 확인
print("{0} 디렉터리의 존재 여부: {1}".format(dir_path, dir_path.exists()))
