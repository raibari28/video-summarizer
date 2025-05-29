from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    url = data.get("url")
    # Your summarizer logic here
    return jsonify({"summary": f"Summarized content for {url}"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
