from fastapi import FastAPI 
from pydantic import BaseModel

app = FastAPI()

class Info(BaseModel):
    id : int
    name:str

@app.get('/')
def healthCheck():
    return "OK"

@app.post('/select/test')
def selectTest(info: Info):
    data = info.dict()
    print(type(data))
    
    return data
