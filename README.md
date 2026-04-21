# RAG-Based Mutual Fund FAQ Chatbot

## 📌 Project Overview
This project is a Retrieval-Augmented Generation (RAG) chatbot that answers factual questions about mutual fund schemes using only official public sources. The chatbot is designed to provide concise, verifiable information such as expense ratio, exit load, minimum SIP, lock-in period, and statement download process.

It strictly follows a **facts-only approach** and does not provide investment advice.

---

## 🏢 Selected AMC and Schemes

**AMC:** HDFC Asset Management Company

**Schemes Covered:**
- HDFC Top 100 Fund (Large Cap)
- HDFC Flexi Cap Fund
- HDFC ELSS Tax Saver Fund
- HDFC Balanced Advantage Fund

---

## 📚 Data Sources

The chatbot uses only official and trusted public sources:

- Groww scheme pages  
- HDFC AMC official website  
- AMFI (Association of Mutual Funds in India)  
- SEBI (Securities and Exchange Board of India)  
- CAMS & KFintech (for statements and reports)  

Source list available in: `data/sources.csv`

---

## ⚙️ Tech Stack

- **Backend:** FastAPI  
- **Frontend:** Streamlit  
- **Vector Database:** ChromaDB  
- **Embeddings:** sentence-transformers/all-MiniLM-L6-v2 (used during ingestion)  
- **LLM:** Groq (LLaMA 3.1 8B Instant)  

---

## 🧠 How It Works

1. Data is collected from official public sources  
2. Text is cleaned and split into smaller chunks  
3. Embeddings are generated and stored in ChromaDB  
4. User query is matched with relevant chunks (semantic search)  
5. Retrieved context is passed to the Groq LLM  
6. The chatbot generates a concise answer with a source link  

---

## 🚀 Live Deployment

- **Frontend (Streamlit):**  
  https://rag-mf-chatbot-1.streamlit.app/

- **Backend (Render):**  
  https://rag-mf-chatbot-1.onrender.com

---

## ▶️ How to Run Locally

```bash
git clone https://github.com/srvadranapu-lab/rag-mf-chatbot.git
cd rag-mf-chatbot

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Run backend
uvicorn app.main:app --reload

# Run frontend
streamlit run frontend/app.py