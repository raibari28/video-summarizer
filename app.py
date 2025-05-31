import os
from flask import Flask, request, jsonify
import yt_dlp
import whisper
from transformers import pipeline

app = Flask(__name__)

# Set up summarizer pipeline (loads model at startup)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def download_audio(url, output_path="audio.mp3"):
    # Remove existing file if present
    if os.path.exists(output_path):
        os.remove(output_path)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path

def transcribe(audio_path, model_size="base"):
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result['text']

def chunk_text(text, chunk_size=1000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def summarize_text(text, max_length=130, min_length=30):
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

def summarize_long_text(text):
    chunks = chunk_text(text)
    summaries = [summarize_text(chunk) for chunk in chunks]
    return "\n".join(summaries)

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"error": "No URL provided."}), 400
    try:
        audio_path = download_audio(url)
        transcript = transcribe(audio_path)
        summary = summarize_long_text(transcript)
        return jsonify({
            "summary": summary,
            "transcript": transcript
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # For Railway, use 0.0.0.0 and port from $PORT env var
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
