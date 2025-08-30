## **flutter-ai-chat-backend**
This is the backend source code for a **multifunctional AI chat application** built with **Flask + PostgreSQL** and integrated with several AI services including **OpenAI API, Replicate API (Google/Imagen-4), and Runway API (gen4_turbo)**.

The server handles a variety of AI-driven tasks for the frontend (Flutter, iOS, Android), including:

- Text-based chat responses using GPT models
- Image generation and analysis
- Audio transcription and understanding
- Video generation from images and text prompts
- Multimodal processing that combines text, images, and audio

It provides a unified API to send user inputs and receive AI-generated content, making it a versatile backend for chatbots, virtual avatars, and multimedia AI applications.


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
👉 http://127.0.0.1:5000/understand_audio<br>
👉 http://127.0.0.1:5000/generate_image<br>
👉 http://127.0.0.1:5000/understand_image<br>
👉 http://127.0.0.1:5000/generate_video<br>
👉 http://127.0.0.1:5000/multimodal<br>


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

#### 3. Avatar API (Chat + TTS + Lip-Sync Data)
Understand the content of an audio file and return a text answer using **OpenAI GPT-4o-mini**.
```
curl -X POST http://127.0.0.1:5000/understand_audio \
  -H "Content-Type: application/json" \
  -d '{
        "audio_url": "https://hpscript.s3.ap-northeast-1.amazonaws.com/voice.wav"
      }'
```
Response (example):
```
{"transcript": "AIチャットでよく聞かれることは何ですか?", "answer": "AIチャットでよく聞かれることはいくつかありますが、以下のような質問が一般的です。\n\n1. **情報提供**:\n   - 歴史的な出来事や文化に関する質問\n   - 科学や技術に関する基本的な情報\n\n2. **助言や提案**:\n   - 健康や生活に関するアドバイス\n   - 学習方法やキャリアに関する相談\n\n3. **トラブルシューティング**:\n   - コンピュータやソフトウェアの問題解決\n   - 日常生活でのトラブルへの対処法\n\n4. **エンターテイメント**:\n   - 映画や本のおすすめ\n   - ジョークやクイズ\n\n5. **雑学や豆知識**:\n   - 面白い事実や trivia\n   - 特定のテーマに関する詳細\n\n6. **技術的な質問**:\n   - プログラミングやコンピュータサイエンスに関する質問\n   - AIや機械学習の仕組み\n\nこれらの質問に対して、できる限り正確かつ詳細な情報を提供することが求められます。", "metadata": {"model": "gpt-4o-mini", "created": "20250824032605"}}
```
- The `transcript` field contains the text of the spoken content in the audio file.  
- The `answer` field contains the model's response to the content of the audio.  
- Metadata includes the model name and timestamp of generation.  

#### 4. Generate Image API
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

#### 5. Understand Image API
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
- The API accepts any image URL and a question in Japanese or English.<br>
- The response contains the AI’s answer and metadata including the model used and timestamp.

#### 6. Generate Video API
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

#### 7. Multimodal API (Text + Image + Audio)
Analyze text, images, and audio simultaneously using OpenAI GPT-4o-mini.
- text → question or instruction
- image_url → image URL
- audio_url → audio URL (mp3/wav)
```
curl -X POST http://127.0.0.1:5000/multimodal \
  -H "Content-Type: application/json" \
  -d '{
        "text": "猫について説明してください",
        "image_url": "https://hpscript.s3.ap-northeast-1.amazonaws.com/cat.jpg",
        "audio_url": "https://hpscript.s3.ap-northeast-1.amazonaws.com/cat_voice.mp3"
      }'
```
Response (example):
```
{
  "image_analysis": {
    "question": "猫について説明してください",
    "answer": "猫は、小型の霊長類に属する哺乳動物で、特に家畜として人気があります。彼らは独立心が強く、警戒心もある一方で、愛情深く飼い主と強い絆を結ぶことができます。\n\n### 基本的な特徴\n\n- **体型**: スリムで柔軟、俊敏な体を持ち、約3〜5キログラムから10キログラム程度の大きさ。\n- **被毛**: 短毛種と長毛種があり、さまざまな色と模様があります。\n- **感覚**: 優れた視覚と聴覚を持ち、夜行性で、夜間でもよく見えます。\n\n### 行動\n\n- **社会性**: 一般的に、猫は独りで過ごすのが好きですが、一緒に遊んだり過ごしたりすることで、社会的な結びつきを形成します。\n- **習性**: 獲物を捕まえるための狩猟本能を持ち、遊ぶことを通じてこの本能を発揮します。\n\n### 飼い方\n\n- **飼育環境**: 家庭内での飼育に適し、必要な環境を整えることで健康的に育てることができます。\n- **食事**: 肉食性で、猫用の餌を提供することが重要です。\n\n多くの家庭で愛される存在であり、ストレスを軽減する効果もあるとされています。",
    "metadata": {
      "model": "gpt-4o-mini",
      "created": "20250824202654"
    }
  },
  "audio_analysis": {
    "transcript": "Meow!",
    "answer": "「ニャー！」という猫の鳴き声を表現しています。これは猫が自分の存在を知らせたり、何かを要求したりする際によく使う音です。",
    "metadata": {
      "model": "gpt-4o-mini",
      "created": "20250824202658"
    }
  },
  "text_response": {
    "answer": "テキスト入力『猫について説明してください』に基づき応答します。"
  }
}
```
- image_analysis.answer → AI explanation based on the image
- audio_analysis.transcript → Transcribed text from the audio
- audio_analysis.answer → Japanese/English explanation of the audio content
- text_response.answer → Response based on the input text
- Supports Japanese and English, with proper UTF-8 encoding

## Note 
- The frontend (Flutter app) will call this backend API.
- Make sure PostgreSQL is running before starting the server.
- Audio files are generated under the audio/ directory and served via /audio/<filename>.
- Image files are generated under the images/ directory and served via /images/<filename>.
- Video files are generated under the videos/ directory and served via /video/<filename>.

## Frontend Demo
<p align="left">
<img src="https://hpscript.s3.ap-northeast-1.amazonaws.com/ios_demo.png" alt="sample image" width="30%">
</p>