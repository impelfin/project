from fastapi import FastAPI 
import requests

app = FastAPI()

@app.get('/')
def healthCheck():
    return "OK"

@app.get('/selectdata')
def selectData():
    param = {"loc":["query","id"]}
    result = requests.get('http://192.168.1.64:3000/getMongo', params=param)
    print(result.json())
    return 
