import json

python_dict = {
    "이름": "홍길동",
    "나이": 25,
    "거주지": "서울",
    "신체정보": {
        "키": 175.4,
        "몸무게": 71.2
    },
    "취미": [
        "등산",
        "자전거타기",
        "독서"
    ]
}

json_data = json.dumps(python_dict, indent=3, sort_keys=True, ensure_ascii=False)

dict_data = json.loads(json_data) # JSON 형식의 데이터를 파이썬의 딕셔너리로 변환
print(type(dict_data))

print(dict_data['신체정보']['몸무게'])

print(dict_data['취미'])

print(dict_data['취미'][0])