## **flutter-ai-chat-backend**
This is the backend source code for the AI chat app using **Flask + PostgreSQL + OpenAI API + Replicate API (Google/Imagen-4)**.  
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
REPLICATE_API_TOKEN=
```

### Step 3. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install flask psycopg2-binary openai python-dotenv gTTS pydub numpy replicate
```

### Step 4. Run Server
```
python3 app.py
```

The Flask server will start at:<br>
👉 http://127.0.0.1:5000/chat<br>
👉 http://127.0.0.1:5000/avatar<br>
👉 http://127.0.0.1:5000/generate_image<br>


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

#### 3. Generate Image API
Generate images from text prompts using **Replicate API (Google/Imagen-4)**.
```
curl -X POST http://127.0.0.1:5000/generate_image \
  -H "Content-Type: application/json" \
  -d '{"prompt": "an astronaut riding a horse on mars, hd, dramatic lighting"}'
```
Response (example):
```
{
  "prompt": "an astronaut riding a horse on mars, hd, dramatic lighting",
  "image_url": "http://127.0.0.1:5000/image/image_20250823034938.png",
  "metadata": {
    "model": "google/imagen-4",
    "created": "20250823034938"
  }
}
```
- The generated images are saved in the images/ directory on the server.
- You can access them directly via the returned image_url.

## Note 
- The frontend (Flutter app) will call this backend API.
- Make sure PostgreSQL is running before starting the server.
- Audio files are generated under the audio/ directory and served via /audio/<filename>.
- Image files are generated under the images/ directory and served via /images/<filename>.