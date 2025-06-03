import importlib
import os
import sys
import types

# Ensure the project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Stub heavy dependencies so app can be imported without installing them
flask_stub = types.ModuleType("flask")

class DummyFlask:
    def route(self, *a, **k):
        def decorator(func):
            return func
        return decorator

flask_stub.Flask = lambda *a, **k: DummyFlask()
flask_stub.request = None
flask_stub.jsonify = lambda *a, **k: None
sys.modules.setdefault("flask", flask_stub)

sys.modules.setdefault("requests", types.ModuleType("requests"))

yt_stub = types.ModuleType("yt_dlp")
yt_stub.YoutubeDL = object
sys.modules.setdefault("yt_dlp", yt_stub)

sys.modules.setdefault("whisper", types.ModuleType("whisper"))

trans_stub = types.ModuleType("transformers")
trans_stub.pipeline = lambda *a, **k: None
sys.modules.setdefault("transformers", trans_stub)

app = importlib.import_module("app")

def test_chunk_text_basic():
    assert app.chunk_text("abcde", chunk_size=2) == ["ab", "cd", "e"]
