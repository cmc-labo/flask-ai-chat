## **flutter-ai-chat-backend**
This is the backend source code for the AI chat app using **Flask + PostgreSQL + OpenAI API + Replicate API (Google/Imagen-4) + Runway API (gen4_turbo)**.  
It receives chat messages from the frontend (Flutter, iOS/Android) and returns AI-generated responses or media.


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
RUNWAY_API_KEY=
```

### Step 3. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install flask psycopg2-binary openai python-dotenv gTTS pydub numpy replicate runwayml
```

### Step 4. Run Server
```
python3 app.py
```

The Flask server will start at:<br>
👉 http://127.0.0.1:5000/chat<br>
👉 http://127.0.0.1:5000/avatar<br>
👉 http://127.0.0.1:5000/generate_image<br>
👉 http://127.0.0.1:5000/generate_video<br>


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
<img src="https://hpscript.s3.ap-northeast-1.amazonaws.com/astronaut_house.png" alt="sample image" width="50%">
- The generated images are saved in the images/ directory on the server.
- You can access them directly via the returned image_url.

#### 4. Understand Image API
Analyze an image and ask questions about it using OpenAI GPT-4o-mini.
```
curl -X POST http://127.0.0.1:5000/understand_image \
  -H "Content-Type: application/json" \
  -d '{
        "question": "この犬の犬種は何ですか？",
        "image_url": "https://hpscript.s3.ap-northeast-1.amazonaws.com/dog.jpg"
      }'
```
Response (example):
```
{
  "question": "この犬の犬種は何ですか？",
  "answer": "この犬はアラスカン・マラミュートという犬種のようです。大型で力強い犬で、主にそり引きとして飼育されています。特徴的な毛色と穏やかな性格が魅力です。",
  "metadata": {
    "model": "gpt-4o-mini",
    "created": "20250824022922"
  }
}
```
<img src="https://hpscript.s3.ap-northeast-1.amazonaws.com/dog.jpg" width="50%">
- The API accepts any image URL and a question in Japanese or English.
- The response contains the AI’s answer and metadata including the model used and timestamp.

#### 5. Generate Video API
Generate short videos from an image + text prompt using Runway API (gen4_turbo).
```
curl -X POST http://127.0.0.1:5000/generate_video \
  -H "Content-Type: application/json" \
  -d '{
        "prompt": "宇宙船が飛ぶ街",
        "prompt_image": "https://hpscript.s3.ap-northeast-1.amazonaws.com/space.jpg",
        "duration": 5
      }'
```
Response (example):
```
{
  "prompt": "宇宙船が飛ぶ街",
  "video_url": "http://127.0.0.1:5000/video/video_20250823181941.mp4",
  "metadata": {
    "model": "gen4_turbo",
    "duration": 5,
    "created": "20250823181941"
  }
}
```
<a href="https://hpscript.s3.ap-northeast-1.amazonaws.com/spacecraft.mp4">
  <img src="https://hpscript.s3.ap-northeast-1.amazonaws.com/space_craft.png" width="50%">
</a><br>

- The generated video is saved in the videos/ directory on the server.
- You can access it directly via the returned video_url.
- Note: duration must be 5 or 10 seconds due to API constraints.

## Note 
- The frontend (Flutter app) will call this backend API.
- Make sure PostgreSQL is running before starting the server.
- Audio files are generated under the audio/ directory and served via /audio/<filename>.
- Image files are generated under the images/ directory and served via /images/<filename>.
- Video files are generated under the videos/ directory and served via /video/<filename>.