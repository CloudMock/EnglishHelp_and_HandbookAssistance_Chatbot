from flask import Flask, request, jsonify, Response
import requests
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OLLAMA_URL = "http://localhost:11434/api/generate"  # Ollama 默认地址
MODEL_NAME = "english-help"

@app.route("/chat", methods=["GET", "POST"])
def chat():
    user_input = request.json.get("message", "")
    print(f"Received message: {user_input}")
    
    if not user_input:
        return jsonify({"error": "Message cannot be empty"}), 400

    payload = {
        "model": MODEL_NAME,
        "prompt": user_input,
        "stream": False  # 设为 True 可以流式返回
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response_json = response.json()

        # 确保返回的 JSON 是 UTF-8 编码
        return Response(
            json.dumps({"response": response_json.get("response", "")+ "\n"}, ensure_ascii=False, indent=4),
            mimetype='application/json;charset=utf-8'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)