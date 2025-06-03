# Video Summarizer

Summarize YouTube and other video content locally using ASR (Whisper) and text summarization (BART), with an API suitable for Custom GPT integration.

## Features

- Download & extract audio from video links (YouTube, etc)
- Transcribe audio to text using Whisper
- Summarize transcript with BART transformer
- REST API endpoint (`/summarize`) for integration (e.g. with GPTs)
- Docker-ready for easy deployment (Railway, Hugging Face Spaces, etc)

## Quickstart

### 1. Clone & Install

```bash
git clone https://github.com/raibari28/video-summarizer.git
cd video-summarizer
pip install -r requirements.txt
```

### 2. Run Tests

```bash
pytest
```