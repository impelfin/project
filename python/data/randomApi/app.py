from fastapi import FastAPI 
import random

app = FastAPI()

@app.get('/')
def healthCheck():
    return "OK"

@app.get('/getrandom')
def recursive_randomInt(count):
    alist=[]      
    n = 10
    while count == 0:
        print(alist)
        return alist
    a = random.randint(1, n) 
    while a in alist:
        a = random.randint(1, n) 
    alist.append(a)
    count -= 1
    recursive_randomInt(count)
    return alist
