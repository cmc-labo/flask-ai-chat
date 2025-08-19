from flask import Flask, request, Response, jsonify, send_file, url_for
from gtts import gTTS
from pydub import AudioSegment
import numpy as np
import json
import psycopg2
import os
import uuid
from openai import OpenAI

app = Flask(__name__)

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", 5432)
}

AUDIO_DIR = "audio_cache"
os.makedirs(AUDIO_DIR, exist_ok=True)


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

@app.route("/avatar", methods=["POST"])
def avator_response():
    data = request.json
    user_text = data.get("text", "")

    # 1. Creating a reply using ChatGPT etc. (This is a simple example)
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful avatar assistant."},
            {"role": "user", "content": user_text}
        ]
    )
    reply_text = completion.choices[0].message.content

    # 2. TTS speech generation
    tts = gTTS(text=reply_text, lang='ja')
    audio_filename = os.path.join(AUDIO_DIR, f"output_{uuid.uuid4().hex}.mp3")
    tts.save(audio_filename)

    # 3. Convert MP3 to WAV using pydub
    wav_filename = audio_filename.replace(".mp3", ".wav")
    sound = AudioSegment.from_mp3(audio_filename)
    sound.export(wav_filename, format="wav")

    # 4. Audio data analysis (amplitude calculation for lip-syncing)
    audio = AudioSegment.from_wav(wav_filename)
    samples = np.array(audio.get_array_of_samples())
    if audio.channels == 2:
        samples = samples.reshape((-1, 2)).mean(axis=1)
    samples = samples / np.max(np.abs(samples))  # Normalize

    # Frame-by-frame amplitude sampling
    fps = 30
    samples_per_frame = int(audio.frame_rate / fps)
    lip_sync = []
    for i in range(0, len(samples), samples_per_frame):
        frame = samples[i:i + samples_per_frame]
        lip_sync.append(float(np.abs(frame).mean()))

    # 5. Return to client
    response_data = {
        "text": reply_text,
        "audio_url": url_for("get_audio", filename=os.path.basename(wav_filename), _external=True),
        "lip_sync": lip_sync
    }

    return Response(json.dumps(response_data, ensure_ascii=False), mimetype="application/json")

@app.route("/audio/<filename>", methods=["GET"])
def get_audio(filename):
    file_path = os.path.join(AUDIO_DIR, filename)
    return send_file(file_path, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)