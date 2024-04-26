from fastapi import FastAPI 
import pandas as pd 
import numpy as np

app = FastAPI()

@app.get('/')
def healthCheck():
    return "OK"

@app.get('/getcsv')
def getcsv():
    csv_file = 'seoul_hospital.csv'

    df = pd.read_csv(csv_file)
    print(df)
    xdf = df['좌표정보(X)'].fillna('111')
    
    print(xdf)
    print(xdf.isna().sum())
    # rows = list(df['좌표정보(X)'])
    
    # print(df)
    return  