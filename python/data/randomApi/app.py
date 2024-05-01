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
        n = 10
        max = 10
    elif (n is None and max is not None):
        n = 10
        max = int(max)
    elif max == None:
        n = int(n)
        max = 10
    else:
        n = int(n)
        max = int(max)
    for i in range(n):
        a = random.randint(1, max) 
        while a in alist:
            a = random.randint(1, max) 
        alist.append(a)
    print({'resultCode' : 200, 'n' : n, 'max' : max, 'result' : alist})
    return {'resultCode' : 200, 'n' : n, 'max' : max, 'result' : alist}
