from fastapi import FastAPI
import pandas as pd

app = FastAPI()

rowData = {
  "page": 1,
  "per_page": 6,
  "total": 12,
  "total_pages": 14,
  "data": [
    {
      "id": 1,
      "name": "cerulean",
      "year": 2000,
      "color": "#98B2D1",
      "pantone_value": "15-4020"
    },
    {
      "id": 2,
      "name": "fuchsia rose",
      "year": 2001,
      "color": "#C74375",
      "pantone_value": "17-2031"
    },
    {
      "id": 3,
      "name": "true red",
      "year": 2002,
      "color": "#BF1932",
      "pantone_value": "19-1664"
    },
    {
      "id": 4,
      "name": "aqua sky",
      "year": 2003,
      "color": "#7BC4C4",
      "pantone_value": "14-4811"
    },
    {
      "id": 5,
      "name":"green",
      "year": 2004,
      "color": "#E2583E",
      "pantone_value": "17-1456"
    },
    {
      "id": 6,
      "name": "blue turquoise",
      "year": 2005,
      "color": "#53B0AE",
      "pantone_value": "15-5217"
    }
  ]
}

@app.get('/')
async def healthcheck():
    return "OK"

@app.get('/getdata')
async def getdata():
    print(rowData)
    return rowData

@app.get('/makeframe')
async def makeframe():
    listData = rowData['data']
    data = []
    for i in range(len(listData)):
        row = {"name" : listData[i]['name'], "year": listData[i]['year']}
        data.insert(i, row)
    # print("data : ", data)
    item = ['name', 'year']
    df = pd.DataFrame(data, columns=item)
    print(df)
    return f'result : {data}'