from get_context import get_recent_chat_context
import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="114514",
        database="EHAHC"
    )
    return connection

def print_context(messages):
    if not messages:
        print("✅ 数据库为空，返回空列表。")
        return

    print("✅ 成功获取聊天记录：")
    for msg in messages:
        print(f"{msg['role']}: {msg['content']}")

if __name__ == "__main__":
    conn = get_db_connection()
    try:
        messages = get_recent_chat_context(conn, 10)
        print_context(messages)
    finally:
        conn.close()