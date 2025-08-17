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
pip install flask psycopg2-binary openai python-dotenv
```

### Step 4. Run Server
```
python3 app.py
```

The Flask server will start at:
👉 http://127.0.0.1:5000/chat

### Step 5. Test API
```
curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "12345", "message": "おはよう！"}'
```

```
{
  "reply": "おはようございます！元気ですか？何かお手伝いできることがありますか？"
}
```

## Note 
- The frontend (Flutter app) will call this backend API.
- Make sure PostgreSQL is running before starting the server.