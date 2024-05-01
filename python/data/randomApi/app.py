from fastapi import FastAPI 
import random

app = FastAPI()

@app.get('/')
def healthCheck():
    return "OK"

@app.get('/getrandom')
def randomInt(n=None, max=None):
    alist=[]    
    if (n and max) == None:
        n = 5
        max = 5
    elif n == None :
        n = 5
    elif max == None:
        max = 5
    else:
        n = int(n)
        max = int(max)
    for i in range(n):
        a = random.randint(1, max) 
        while a in alist:
            a = random.randint(1, max) 
        alist.append(a)
    return alist
