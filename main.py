from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class VideoURL(BaseModel):
    url: str

@app.post("/summarize")
def summarize(data: VideoURL):
    return {"summary": f"Dummy summary for {data.url}"}
