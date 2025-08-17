from flask import Flask, request, Response
import json
import psycopg2
import os
from openai import OpenAI

app = Flask(__name__)

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", 5432)
}


def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        user_id = data.get("user_id")
        message = data.get("message")

        if not user_id or not message:
            return Response(json.dumps({"error": "user_id and message are required"}), status=400, content_type="application/json; charset=utf-8")

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO chat_messages (user_id, message) VALUES (%s, %s) RETURNING id;",
            (user_id, message)
        )
        chat_id = cur.fetchone()[0]

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )
        api_reply = completion.choices[0].message.content

        cur.execute(
            "UPDATE chat_messages SET reply = %s WHERE id = %s;",
            (api_reply, chat_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        

        response_json = json.dumps({"reply": api_reply}, ensure_ascii=False)
        return Response(response_json, content_type="application/json; charset=utf-8")

    except Exception as e:
        error_json = json.dumps({"error": str(e)}, ensure_ascii=False)
        return Response(error_json, status=400, content_type="application/json; charset=utf-8")


if __name__ == "__main__":
    app.run(debug=True)