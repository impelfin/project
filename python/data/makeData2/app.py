from fastapi import FastAPI 
from pandas import Series
import pandas as pd 

app = FastAPI()

@app.get('/')
def healthCheck():
    return "OK"

@app.get('/getcsv')
def getcsv():
    csv_file = 'seoul_hospital.csv'

    df = pd.read_csv(csv_file)

    orgdf = df[['사업장명', '업태구분명']]
    # orgdf = df.loc[:,['사업장명', '업태구분명']]

    # 울릉도 => 위도 : 1300026.73, 경도 : 1948720.66
    xdf = df['좌표정보(X)']
    xdf = xdf.fillna('1300026.73')
    ydf = df['좌표정보(Y)']
    ydf = ydf.fillna('1948720.66')
    
    newdf = pd.concat([orgdf, xdf, ydf], axis=1)
    print(newdf)

    # print(newdf.isna().sum())
    newdf = dict(newdf)
    return f'result: {newdf}'
