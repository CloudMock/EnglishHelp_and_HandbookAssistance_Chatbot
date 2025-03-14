from flask import Flask, request, jsonify, Response
import requests
import json

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate" # localhost change to ip address
MODEL_NAME = "llama3"  # choose modle installed

@app.route("/chat", methods=["GET", "POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "Message cannot be empty"}), 400

    payload = {
        "model": MODEL_NAME,
        "prompt": user_input,
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response_json = response.json()

        # ensure return JSON is UTF-8
        return Response(
            json.dumps({"response": response_json.get("response", "")+ "\n"}, ensure_ascii=False, indent=4),
            mimetype='application/json;charset=utf-8'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)

