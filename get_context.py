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
