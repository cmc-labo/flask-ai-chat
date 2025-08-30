import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(api_key=api_key)

docs = [
    "LangChainは、LLMを活用したアプリ開発を効率化するフレームワークです。",
    "RAGは、外部の知識を検索してLLMに渡すことで精度の高い応答を生成する手法です。",
    "FAISSはベクトル検索用の高速ライブラリで、LangChainでRAGを実装する際によく使われます。"
]

vectorstore = FAISS.from_texts(docs, embeddings)

llm = OpenAI(temperature=0.7, api_key=api_key)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever()
)

question = "RAGとは何ですか？"
answer = qa.run(question)
print("質問:", question)
print("回答:", answer)