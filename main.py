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
    # Download and transcribe the video/audio, then return summary/transcript.
    try:
        # 1. Download audio with yt_dlp, prefer mp3/m4a
        ydl_opts = {
            'format': 'bestaudio[ext=mp3]/bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': 'audio.%(ext)s',
            'quiet': True,
            'noplaylist': True,
            'cookiefile': 'cookies.txt'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(data.url, download=True)
            downloaded_file = ydl.prepare_filename(info)

        # 2. Load Whisper model (tiny)
        model = whisper.load_model("tiny")

        # 3. Transcribe audio file
        result = model.transcribe(downloaded_file)
        transcript = result.get("text", "")

        # 4. Clean up all audio files (mp3/m4a/others)
        for f in glob.glob("audio.*"):
            try:
                os.remove(f)
            except Exception:
                pass

        # 5. Return transcript as summary
        return {"summary": transcript[:4000]}

    except Exception as e:
        # Clean up any leftover audio files
        for f in glob.glob("audio.*"):
            try:
                os.remove(f)
            except Exception:
                pass
        # Return a clear error message
        raise HTTPException(status_code=500, detail=f"Failed to summarize video: {str(e)}")
