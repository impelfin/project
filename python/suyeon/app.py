from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import os
from botocore.exceptions import ClientError, BotoCoreError

api_key = os.getenv('OPENAI_API_KEY')
app = FastAPI()

polly_client = boto3.client('polly', region_name='ap-northeast-2')

class TextToSpeechRequest(BaseModel):
  text: str
  voice_id: str = 'Seoyeon'

@app.get("/")
def Hello():
  return "Hello World!"

@app.post("/text-to-speech/")
async def text_to_speech(request: TextToSpeechRequest):
    try:
        # Amazon Polly 호출
        response = polly_client.synthesize_speech(
            Text=request.text,
            OutputFormat='mp3',
            VoiceId=request.voice_id
        )

        # 오디오 스트림을 파일로 저장
        audio_stream = response.get('AudioStream')
        if audio_stream:
            with open('output.mp3', 'wb') as file:
                file.write(audio_stream.read())

            return {"message": "Text converted to speech successfully", "file": "output.mp3"}

    except (BotoCoreError, ClientError) as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"message": "Failed to convert text to speech"}
    
@app.get("/download-audio/")
async def download_audio():
    file_path = 'output.mp3'
    if os.path.exists(file_path):
        return FileResponse(path=file_path, media_type='audio/mpeg', filename='output.mp3')
    else:
        raise HTTPException(status_code=404, detail="File not found")

if __name__ == '__main__' :
  uvicorn.run(app, host="0.0.0.0", port=3000)
