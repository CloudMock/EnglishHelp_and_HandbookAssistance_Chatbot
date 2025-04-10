<<<<<<< HEAD
from flask import Flask, request, jsonify, Response
=======
# pip install flask mysql-connector-python bcrypt flask-jwt-extended

from flask import Flask, request, jsonify, Response, session
import requests
>>>>>>> origin/dev
import json
import mysql.connector
from mysql.connector import Error
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from ollama import generate

app = Flask(__name__)
CORS(app)

<<<<<<< HEAD
@app.route("/chat", methods=["GET", "POST"])
def chat():
    user_input = request.json.get("message", "")
    
    if not user_input:
        return jsonify({"error": "Message cannot be empty"}), 400
    
    try:
        response = generate(model='english-help', prompt=user_input)
        response_content = response.response
        
        if not response_content:
            raise ValueError("Ollama 返回的 JSON 为空")

        # ensure return JSON is UTF-8
        return Response(
            json.dumps({"response": response_content}, ensure_ascii=False, indent=4),
            mimetype='application/json;charset=utf-8'
        )
    
=======
app.config["JWT_SECRET_KEY"] = "your_secret_key"  # Replace with a more secure key
jwt = JWTManager(app)

# OLLAMA configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

# Connecting to a database
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",       # Replace with your database username
            password="114514",  # Replace with your database password
            database="EHAHC"
        )
        return connection
    except Error as e:
        print(f"Database connection failed: {e}")
        return None

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

    # 哈希密码
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

# Handling chat
@app.route("/chat", methods=["POST"])
@jwt_required()
def chat():
    user_input = request.json.get("message", "")
    curtin_id = get_jwt_identity()  # Get the current user's Curtin_ID
    if not user_input:
        return jsonify({"error": "Message cannot be empty"}), 400

    payload = {
        "model": MODEL_NAME,
        "prompt": user_input,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response_json = response.json()
        bot_response = response_json.get("response", "") + "\n"

        # Store chat history
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Chat_history (Student_input, Bot_answer, Curtin_ID) VALUES (%s, %s, %s)",
                           (user_input, bot_response, curtin_id))
            conn.commit()
            cursor.close()
            conn.close()

        return Response(json.dumps({"response": bot_response}, ensure_ascii=False, indent=4),
                        mimetype='application/json;charset=utf-8')
>>>>>>> origin/dev
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
<<<<<<< HEAD
    app.run(debug=True, port=5000)
=======
    app.run(debug=True, port=5000)

>>>>>>> origin/dev
