from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import uvicorn

app = FastAPI()

class VideoURL(BaseModel):
    url: str

@app.post("/summarize")
def summarize(data: VideoURL):
    # Return a fast dummy summary
    return {"summary": f"Dummy summary for {data.url}"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
