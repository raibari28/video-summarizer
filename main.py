from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yt_dlp
import whisper
import os

app = FastAPI()

class VideoURL(BaseModel):
    url: str

@app.post("/summarize")
def summarize(data: VideoURL):
    # Download and transcribe the video/audio, then return summary/transcript.
    output_file = "audio.m4a"
    try:
        # 1. Download audio with yt_dlp
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]',
            'outtmpl': output_file,
            'quiet': True,
            'noplaylist': True,
            'cookiefile': 'cookies.txt'   # <--- add this line!
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([data.url])

        # 2. Load Whisper model (tiny)
        model = whisper.load_model("tiny")

        # 3. Transcribe audio file
        result = model.transcribe(output_file)
        transcript = result.get("text", "")

        # 4. Clean up audio file
        if os.path.exists(output_file):
            os.remove(output_file)

        # 5. Return transcript as summary
        return {"summary": transcript[:4000]}

    except Exception as e:
        # Clean up in case of error
        if os.path.exists(output_file):
            os.remove(output_file)
        # Return a clear error message
        raise HTTPException(status_code=500, detail=f"Failed to summarize video: {str(e)}")
