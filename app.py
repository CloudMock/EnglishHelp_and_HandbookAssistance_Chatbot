from flask import Flask, request, jsonify, Response
import json
from sentence_transformers import SentenceTransformer
import faiss
import mysql.connector
from mysql.connector import Error
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import ollama

app = Flask(__name__)
CORS(app)

# load embedding model and index
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
index = faiss.read_index("Faiss/store/student_handbook_faiss.index")

# read txt chunks
with open("Faiss/store/text_chunks.txt", "r", encoding="utf-8") as f:
    text_chunks = f.read().split("\n====\n")

# set secure key
app.config["JWT_SECRET_KEY"] = "your_secret_key"  # Replace with a more secure key
jwt = JWTManager(app)

# Connect to a database
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="ehahc",
            password="114514",
            database="EHAHC"
        )
        return connection
    except Error as e:
        print(f"Database connection failed: {e}")
        return None

# get context from database
def get_recent_chat_context(conn, num_QApair):
    
    messages = []
    cursor = conn.cursor(dictionary=True)

    try:
        # Get the most recent n conversations
        query = """
            SELECT Student_input, Bot_answer
            FROM Chat_history
            ORDER BY Use_date DESC
            LIMIT %s
        """
        cursor.execute(query, (num_QApair,))
        rows = cursor.fetchall()

        # reverse to normal word order
        rows.reverse()

        for row in rows:
            messages.append({
                'role': 'user',
                'content': row['Student_input']
            })
            messages.append({
                'role': 'assistant',
                'content': row['Bot_answer']
            })

    finally:
        cursor.close()

    return messages 

# User Registration
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    curtin_id = data.get("Curtin_ID")
    password = data.get("Password")
    name = data.get("Student_name")
    email = data.get("Student_email")

    if not all([curtin_id, password, name, email]):
        return jsonify({"error": "All fields cannot be empty"}), 400

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Student (Curtin_ID, Password, Student_name, Student_email) VALUES (%s, %s, %s, %s)",
                       (curtin_id, hashed_password.decode("utf-8"), name, email))
        conn.commit()
        return jsonify({"message": "Successful registration"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# User login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    curtin_id = data.get("Curtin_ID")
    password = data.get("Password")

    if not curtin_id or not password:
        return jsonify({"error": "Curtin_ID and Password cannot be empty"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Student WHERE Curtin_ID = %s", (curtin_id,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode("utf-8"), user["Password"].encode("utf-8")):
            access_token = create_access_token(identity=curtin_id)
            return jsonify({"message": "Login successful", "token": access_token}), 200
        else:
            return jsonify({"error": "Wrong username or password"}), 401
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# English help
@app.route("/chat", methods=["GET","POST"])
@jwt_required()
def chat():
    # link to database
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 501

    # Get the current user's Curtin_ID
    curtin_id = get_jwt_identity()

    # get user input
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "Message cannot be empty"}), 400

    try:
        # get context add user input to get model response
        messages = get_recent_chat_context(conn, 3)
        messages.append({"role": "user", "content": user_input})
        response = ollama.chat(
            model = 'english-help',
            messages = messages
        )
        response_content = response.message.content
        print(response.message)
        if not response_content:
            raise ValueError("Ollama return empty JSON")
        
        # store in database
        cursor = conn.cursor()
        query = """
            INSERT INTO Chat_history 
            (Student_input, Bot_answer, Curtin_ID) 
            VALUES (%s, %s, %s)
            """
        cursor.execute(query, (user_input, response_content, curtin_id))
        conn.commit()
        cursor.close()
        
        # close database
        conn.close()

        # ensure return JSON is UTF-8
        return Response(
            json.dumps({"response": response_content}, ensure_ascii=False, indent=4),
            mimetype='application/json;charset=utf-8'
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# hanbook search
@app.route('/search', methods=["GET", "POST"])
def search():
    # link to database
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 501
    
    # Get the current user's Curtin_ID
    curtin_id = get_jwt_identity()
    
    # get user input
    user_input = request.json.get("query", "")
    if not user_input:
        return jsonify({"error": "query is required"}), 400
    query_vector = model.encode([user_input]) # Vectorization, embedding user input

    # search handbook content from user input
    k = 3  # count of search result
    distances, indices = index.search(query_vector, k)
    # print("\nQuery Result：")
    # for i, idx in enumerate(indices[0]):
    #     print(f"\nSimilarity ranking {i+1}: ")
    #     print(text_chunks[idx])
    #     print(f"🔹 Similarity (L2 distance): {distances[0][i]}")
    #     print("-" * 40)
    results = []
    for i, idx in enumerate(indices[0]):
        results.append(text_chunks[idx])
    # print(results)

    try:
        # get context add user input to get model response
        messages = get_recent_chat_context(conn, 3)
        search_with_prompt= f"""
        follow below information: {results}
        answer the question: {user_input}
        as briefly as possible
        """
        messages.append({"role": "user", "content": search_with_prompt})
        response = ollama.chat(
            model = 'qwen2',
            messages = messages
        )
        response_content = response.message.content
        
        if not response_content:
            raise ValueError("Ollama return empty JSON")

        # store in database
        cursor = conn.cursor()
        query = """
            INSERT INTO Search_history 
            (Student_input, Bot_answer, Curtin_ID) 
            VALUES (%s, %s, %s)
            """
        cursor.execute(query, (user_input, response_content, curtin_id))
        conn.commit()
        cursor.close()

        # close database
        conn.close()

        # ensure return JSON is UTF-8
        return Response(
            json.dumps({"response": response_content}, ensure_ascii=False, indent=4),
            mimetype='application/json;charset=utf-8'
        )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)