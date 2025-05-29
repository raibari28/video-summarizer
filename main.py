from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yt_dlp
import whisper
import os
import glob

app = FastAPI()

class VideoURL(BaseModel):
    url: str

@app.post("/summarize")
def summarize(data: VideoURL):
    try:
        # Name for the output file (will get actual file name below)
        output_file = "audio.%(ext)s"
        
        # 1. Download audio with yt_dlp (add cookiefile option here)
        ydl_opts = {
            'format': 'bestaudio[ext=mp3]/bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': output_file,
            'quiet': True,
            'noplaylist': True,
            'cookiefile': 'cookies.txt'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(data.url, download=True)
            downloaded_file = ydl.prepare_filename(info)

        # 2. Load Whisper model (tiny)
        model = whisper.load_model("tiny")

        # 3. Transcribe the downloaded audio
        result = model.transcribe(downloaded_file)
        transcript = result.get("text", "")

        # 4. Clean up (optional)
        import glob, os
        for f in glob.glob("audio.*"):
            try:
                os.remove(f)
            except Exception:
                pass

        return {"summary": transcript[:4000]}

    except Exception as e:
        # Clean up on error too
        for f in glob.glob("audio.*"):
            try:
                os.remove(f)
            except Exception:
                pass
        raise HTTPException(status_code=500, detail=f"Failed to summarize video: {str(e)}")

