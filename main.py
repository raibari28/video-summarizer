from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yt_dlp
import whisper

app = FastAPI()
model = whisper.load_model("base")

class VideoURL(BaseModel):
    url: str

@app.post("/summarize")
def summarize(data: VideoURL):
    try:
        output_file = "audio.mp3"
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'audio.%(ext)s',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([data.url])

        result = model.transcribe(output_file)
        transcript = result["text"]

        return {
            "transcript": transcript[:4000]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
