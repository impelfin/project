# pip install python-multipart

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from pathlib import Path
import shutil
import os.path

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
IMG_DIR = os.path.join(BASE_DIR, 'images/')
# SERVER_IMG_DIR = os.path.join('http://192.168.1.53:8000/', IMG_DIR)

@app.get('/')
def healthCheck():
    return "OK"

@app.post("/image")
async def image(image: UploadFile = File(...)):
    filename = IMG_DIR + image.filename
    with open(filename, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return {"filename": image.filename}

@app.get("/get_image")
async def get_image(imagename=None):
    filename = IMG_DIR + imagename
    image_path = Path(filename)
    if not image_path.is_file():
        return {"error": "Image not found on the server"}
    return FileResponse(image_path)
