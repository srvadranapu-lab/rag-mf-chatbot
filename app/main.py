from fastapi import FastAPI
from pydantic import BaseModel
from app.rag import generate_answer

app = FastAPI()

class Query(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "MF RAG API running"}

@app.post("/ask")
def ask_question(query: Query):
    answer = generate_answer(query.question)
    return {"answer": answer}