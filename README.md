# Video Summarizer

Summarize YouTube and other video content locally using ASR (Whisper) and text summarization (BART), with an API suitable for Custom GPT integration.

## Features

- Download & extract audio from video links (YouTube, etc)
- Transcribe audio to text using Whisper
- Summarize transcripts with the BART transformer via a separate endpoint
- REST API endpoints for integration:
  - `/summarize` returns the video transcript
  - `/summarize-transcript` returns the summary
- Docker-ready for easy deployment (Railway, Hugging Face Spaces, etc)

## Quickstart

### 1. Clone & Install

```bash
git clone https://github.com/raibari28/video-summarizer.git
cd video-summarizer
pip install -r requirements.txt
