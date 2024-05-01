from fastapi import FastAPI 
import requests

app = FastAPI()

@app.get('/')
def healthCheck():
    return "OK"

@app.get('/selectdata')
def selectData():
    result = requests.get('http://192.168.1.53:3000/getrandom')
    print(result)
    return result
