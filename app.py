from flask import Flask, request, jsonify, Response
import json
from sentence_transformers import SentenceTransformer
import faiss
from flask_cors import CORS
from ollama import generate

app = Flask(__name__)
CORS(app)

# load embedding model and index
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
index = faiss.read_index("Faiss/store/student_handbook_faiss.index")

# read txt chunks
with open("Faiss/store/text_chunks.txt", "r", encoding="utf-8") as f:
    text_chunks = f.read().split("\n====\n")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    user_input = request.json.get("message", "")
    
    if not user_input:
        return jsonify({"error": "Message cannot be empty"}), 400
    
    try:
        response = generate(model='qwen2', prompt=user_input)
        response_content = response.response
        
        if not response_content:
            raise ValueError("Ollama return empty JSON")

        # ensure return JSON is UTF-8
        return Response(
            json.dumps({"response": response_content}, ensure_ascii=False, indent=4),
            mimetype='application/json;charset=utf-8'
        )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search', methods=["GET", "POST"])
def search():

    query_text = request.json.get("query", "")
    print(query_text)
    if not query_text:
        return jsonify({"error": "query is required"}), 400

    # Vectorization
    query_vector = model.encode([query_text])

    # FAISS search
    k = 3  # count of search result
    distances, indices = index.search(query_vector, k)

    # print("\n🔍 查询结果：")
    # for i, idx in enumerate(indices[0]):
    #     print(f"\n相似度排名 {i+1}: ")
    #     print(text_chunks[idx])
    #     print(f"🔹 相似度(L2 距离): {distances[0][i]}")
    #     print("-" * 40)
        
    results = []
    for i, idx in enumerate(indices[0]):
        results.append(text_chunks[idx])
    
    print(results)

    try:
        response = generate(model='qwen2', prompt=f"follow below information: {results}\n answer the question: {query_text}, as briefly as possible")
        response_content = response.response
        
        if not response_content:
            raise ValueError("Ollama return empty JSON")

        # ensure return JSON is UTF-8
        return Response(
            json.dumps({"response": response_content}, ensure_ascii=False, indent=4),
            mimetype='application/json;charset=utf-8'
        )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)

