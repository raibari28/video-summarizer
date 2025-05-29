
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yt_dlp
import whisper
import os
import uvicorn

app = FastAPI()

class VideoURL(BaseModel):
    url: str

@app.post("/summarize")
def summarize(data: VideoURL):
    try:
        output_file = "audio.m4a"
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]',
            'outtmpl': 'audio.%(ext)s',
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([data.url])

        model = whisper.load_model("tiny")
        result = model.transcribe(output_file)
        transcript = result["text"]

        return {
            "summary": transcript[:4000]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
