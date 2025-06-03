 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/README.md b/README.md
index 106f05c1dd562729dbb295e162146bfb89dbbffe..0199d2a846d0cc1fcc0f2e2f9d94731d3cafeeb6 100644
--- a/README.md
+++ b/README.md
@@ -1,20 +1,21 @@
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
+```
 
EOF
)
