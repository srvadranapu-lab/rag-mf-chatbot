import os
import chromadb
from chromadb.config import Settings
from groq import Groq
from dotenv import load_dotenv
from app.prompts import build_prompt

load_dotenv()

DATA_PATH = "data/raw_docs"

chroma_client = chromadb.Client(Settings(persist_directory="vectorstore"))
collection = chroma_client.get_or_create_collection(name="mf_docs")

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def load_documents():
    docs = []
    for file in os.listdir(DATA_PATH):
        path = os.path.join(DATA_PATH, file)
        with open(path, "r", encoding="utf-8") as f:
            docs.append((file, f.read()))
    return docs

def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def retrieve_context(query, top_k=3):
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    return " ".join(results["documents"][0])

def is_advice_question(query):
    keywords = ["should i", "best", "recommend", "buy", "sell", "good investment"]
    return any(k in query.lower() for k in keywords)

def generate_answer(query):
    if is_advice_question(query):
        return "I'm a facts-only assistant and cannot provide investment advice. Please refer to official sources like AMFI: https://www.amfiindia.com"

    context = retrieve_context(query)
    prompt = build_prompt(context, query)

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()