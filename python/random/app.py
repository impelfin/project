from fastapi import FastAPI, HTTPException
from typing import List
from fastapi.responses import JSONResponse
import random

app = FastAPI()

def random_list(n: int, max_value: int) -> List[int]:
    """
    Return n unique random integers between 1 and max_value inclusive.
    """
    return random.sample(range(1, max_value + 1), n)

@app.get("/", response_class=JSONResponse)
def root():
    return {"resultCode": True}

@app.get("/random", response_model=List[int])
def get_random(n: int, max_value: int):
    if max_value < n:
        raise HTTPException(status_code=400, detail="max_value must be >= n")
    result = random_list(n, max_value)
    print(result)
    return result

# 파일을 직접 실행할 때 FastAPI 서버를 8000번 포트로 구동
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)