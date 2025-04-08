from flask import Flask, request, jsonify, Response
import json
from flask_cors import CORS
from ollama import generate

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["GET", "POST"])
def chat():
    user_input = request.json.get("message", "")
    
    if not user_input:
        return jsonify({"error": "Message cannot be empty"}), 400
    
    try:
        response = generate(model='qwen2', prompt=user_input)
        response_content = response.response
        
        if not response_content:
            raise ValueError("Ollama 返回的 JSON 为空")

        # ensure return JSON is UTF-8
        return Response(
            json.dumps({"response": response_content}, ensure_ascii=False, indent=4),
            mimetype='application/json;charset=utf-8'
        )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)