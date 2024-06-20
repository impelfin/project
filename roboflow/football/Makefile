APP_NAME = monitoring:app
HOST = 0.0.0.0
PORT = 3000

install:
	pip install -r requirements.txt

# 유니콘 서버 실행
run:
	uvicorn $(APP_NAME) --host $(HOST) --port $(PORT) --reload
