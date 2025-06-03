import os
from flask import Flask, request, jsonify
import yt_dlp
import whisper
from transformers import pipeline

app = Flask(__name__)

# (Optional: For Hugging Face Spaces or other environments that restrict caching dirs)
os.environ["HF_HOME"] = "/tmp/hf"
os.environ["TRANSFORMERS_CACHE"] = "/tmp/hf"
os.environ["XDG_CACHE_HOME"] = "/tmp/hf"

# Summarizer pipeline (using BART from Hugging Face)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def download_audio(url, output_path="/tmp/audio.mp3"):
    if os.path.exists(output_path):
        os.remove(output_path)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'quiet': True,
        # Uncomment if using cookies.txt:
        # 'cookiefile': 'cookies.txt',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
    return output_path, info.get("id", ""), info.get("title", ""), info.get("description", "")

def transcribe(audio_path, model_size="base"):
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result["text"]

def chunk_text(text, chunk_size=1000):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def summarize_text(text, max_length=130, min_length=30):
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]["summary_text"]

def summarize_long_text(text):
    chunks = chunk_text(text)
    summaries = [summarize_text(chunk) for chunk in chunks]
    return "\n".join(summaries)

@app.route("/", methods=["GET"])
def home():
    return "✅ Video Summarizer API is running. POST /summarize with {\"url\": \"...\"}"

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided."}), 400
    try:
        audio_path, video_id, title, description = download_audio(url)
        transcript = transcribe(audio_path)
        return jsonify({
            "video_id": video_id,
            "title": title,
            "description": description,
            "transcription": transcript
        })
    except Exception as e:
        error_message = str(e)
        if "cookies" in error_message or "Sign in" in error_message:
            return jsonify({
                "error": "CookieError",
                "message": "The YouTube cookies are invalid or expired. Please re-export cookies.txt from a logged-in YouTube session and upload to the app."
            }), 401
        if "403" in error_message or "Forbidden" in error_message:
            return jsonify({
                "error": "PermissionError",
                "message": "The video requires login or is age-restricted. Please try another public video."
            }), 403
        return jsonify({
            "error": "UnexpectedError",
            "message": error_message
        }), 500

@app.route('/summarize-transcript', methods=['POST'])
def summarize_transcript():
    data = request.get_json()
    transcript = data.get("transcript")
    if not transcript:
        return jsonify({"error": "No transcript provided."}), 400
    try:
        summary = summarize_long_text(transcript)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({
            "error": "SummarizationError",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
