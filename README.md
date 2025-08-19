## **flutter-ai-chat-backend**
This is the backend source code for the AI chat app using **Flask + PostgreSQL + OpenAI API**.  
It receives chat messages from the frontend (Flutter, iOS/Android) and returns AI-generated responses.


## **Setup**
### Step 1. Create Database Table
```sql
CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    reply TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Step 2. Configure Environment Variables
Create a .env file in the project root:
.env
```
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=hoge
DB_HOST=localhost
DB_PORT=5432
OPENAI_API_KEY=
```

### Step 3. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install flask psycopg2-binary openai python-dotenv gTTS pydub numpy
```

### Step 4. Run Server
```
python3 app.py
```

The Flask server will start at:<br>
👉 http://127.0.0.1:5000/chat<br>
👉 http://127.0.0.1:5000/avatar

### Step 5. Test API
#### 1. Chat API
```
curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "12345", "message": "おはよう！"}'
```
Response:

```
{
  "reply": "おはようございます！元気ですか？何かお手伝いできることがありますか？"
}
```

#### 2. Avatar API (Chat + TTS + Lip-Sync Data)
```
curl -X POST http://127.0.0.1:5000/avatar \
  -H "Content-Type: application/json" \
  -d '{"text": "おはよう！"}'
```
Response (example):

```
{
  "text": "おはようございます！今日も頑張りましょう！",
  "audio_url": "http://127.0.0.1:5000/audio/output_12345abcd.wav",
  "lip_sync": [0.0, 0.12, 0.24, ...]
}
```
You can fetch the generated audio file directly:
```
curl -O http://127.0.0.1:5000/audio/output_12345abcd.wav
```

## Note 
- The frontend (Flutter app) will call this backend API.
- Make sure PostgreSQL is running before starting the server.
- Audio files are generated under the audio/ directory and served via /audio/<filename>.