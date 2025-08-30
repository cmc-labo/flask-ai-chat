import os
import psycopg2
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", 5432)
}

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_text(text):
    resp = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return resp.data[0].embedding

def insert_document(content):
    """文書をベクトル化して DB に保存"""
    vector = embed_text(content)
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
        (content, vector)
    )
    conn.commit()
    cur.close()
    conn.close()

def search_documents(query, top_k=3):
    """クエリ embedding でベクトルDB検索"""
    q_vector = embed_text(query)
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(f"""
        SELECT content
        FROM documents
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """, (q_vector, top_k))
    results = [r[0] for r in cur.fetchall()]
    cur.close()
    conn.close()
    return results

def generate_answer(query):
    related_docs = search_documents(query)
    context = "\n".join(related_docs)
    prompt = f"以下の文脈を参考にして質問に答えてください。\n\n文脈:\n{context}\n\n質問: {query}\n回答:"

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

if __name__ == "__main__":
    # 文書の挿入例
    insert_document("Pythonは高水準のプログラミング言語です。")
    insert_document("PostgreSQLはオープンソースのリレーショナルデータベースです。")
    insert_document("OpenAIはAI研究と展開を行う企業です。")

    # 質問応答の例
    question = "Pythonとは何ですか？"
    answer = generate_answer(question)
    print("質問:", question)
    print("回答:", answer)