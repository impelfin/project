from fastapi import FastAPI 
import random

app = FastAPI()

@app.get('/')
def healthCheck():
    return "OK"

@app.get('/getrandom')
def randomInt(n=None, max=None):
    alist=[]
    if n is None and max is not None:
        if int(max) < 10:
            n = int(max)
            max = int(max)
        else:
            n = 10
            max = int(max)
    elif n is not None and max is None:
        n = int(n)
        max = 10
    elif (n and max) is None:
        n = 10
        max = 10
    else:
        n = int(n)
        max = int(max)
        if n > max:
            return f'n은 max보다 작아야 합니다.'
            exit
    for i in range(n):
        a = random.randint(1, max) 
        while a in alist:
            a = random.randint(1, max) 
        alist.append(a)
    print({'resultCode' : 200, 'n' : n, 'max' : max, 'result' : alist})
    return {'resultCode' : 200, 'n' : n, 'max' : max, 'result' : alist}
