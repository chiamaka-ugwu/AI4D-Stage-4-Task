# Retrieval-Augmented Generation (RAG) API

A complete Retrieval-Augmented Generation (RAG) system built with **FastAPI**, **HuggingFace Sentence Transformers**, **ChromaDB**, and **Google Gemini**.

The API allows users to upload documents, automatically perform semantic chunking, generate vector embeddings, store them in ChromaDB, and answer natural language questions using Retrieval-Augmented Generation (RAG).

---

## Features

- FastAPI REST API
- Semantic text chunking
- HuggingFace Sentence Transformer embeddings
- ChromaDB vector database
- Google Gemini LLM for answer generation
- Environment-based configuration using `.env`
- Multiple document upload support
- Semantic similarity search
- Supports TXT, PDF and DOCX documents

---

## Project Structure

```
project/
│
├── main.py                 # FastAPI endpoints
├── rag.py                  # Upload processing and RAG pipeline
├── config.py               # Environment configuration
├── parser.py               # File text extraction
├── chunking.py             # Semantic chunking
├── embeddings.py           # HuggingFace embeddings
├── chroma_client.py        # ChromaDB operations
├── requirements.txt
├── README.md
├── .env
├── uploads/
└── data/
```

---

# Technologies Used

- Python
- FastAPI
- HuggingFace Sentence Transformers
- ChromaDB
- Google Gemini API
- python-dotenv
- PyPDF2
- python-docx

---

# Installation

## 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

---

## 2. Create a virtual environment

Windows

```bash
python -m venv .venv
```

Activate it

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create a `.env` file

Create a file named:

```
.env
```

Add the following variables:

```env
HF_API_KEY=your_huggingface_api_key

EMBED_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2

GEMINI_API_KEY=your_gemini_api_key

LLM_MODEL_NAME=your_supported_gemini_model

CHROMA_DB_HOST=localhost

CHROMA_DB_PORT=8000

RAG_DATA_DIR=./data

CHUNK_LENGTH=500

SERVER_PORT=8001
```

---

# Running the Application

## Step 1: Start ChromaDB

```bash
chroma run
```

By default ChromaDB runs on:

```
http://localhost:8000
```

Leave this terminal running.

---

## Step 2: Start the FastAPI application

Open a new terminal.

Activate the virtual environment.

Run:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8001
```

Swagger documentation:

```
http://127.0.0.1:8001/docs
```

---

# API Endpoints

## Health Check

**GET**

```
/health
```

Returns:

```json
{
  "status": "ok"
}
```

---

## Upload Documents

**POST**

```
/upload
```

Content-Type

```
multipart/form-data
```

Parameter

| Name | Type |
|------|------|
| files | File (multiple supported) |

Example Response

```json
{
  "status": "success",
  "documents_uploaded": 1,
  "chunks_created": 8
}
```

---

## Ask Questions

**POST**

```
/prompt
```

Content-Type

```
application/json
```

Request

```json
{
    "query": "What is FastAPI?"
}
```

Example Response

```json
{
    "answer": "FastAPI is a modern Python web framework used for building APIs.",
    "context_used": [
        "FastAPI is a modern Python web framework..."
    ]
}
```

---

# Supported File Types

- TXT
- PDF
- DOCX

---

# How the RAG Pipeline Works

1. User uploads one or more documents.
2. Documents are saved locally.
3. Text is extracted from each document.
4. The text is divided into semantic chunks.
5. Each chunk is converted into an embedding using the HuggingFace Sentence Transformer model.
6. Embeddings and metadata are stored in ChromaDB.
7. A user submits a question.
8. The question is embedded using the same embedding model.
9. ChromaDB retrieves the most relevant chunks.
10. The retrieved context and question are sent to Gemini.
11. Gemini generates an answer using only the retrieved context.
12. The API returns the generated answer along with the retrieved context.

---

# Testing the API (Postman)

## 1. Test the Health Endpoint

Create a request:

**Method**

```
GET
```

**URL**

```
http://127.0.0.1:8000/health
```

Expected response:

```json
{
    "status": "ok"
}
```

---

## 2. Test the Upload Endpoint

Create a request:

**Method**

```
POST
```

**URL**

```
http://127.0.0.1:8000/upload
```

Go to:

```
Body → form-data
```

Add the following field:

| Key | Type | Value |
|------|------|------|
| files | File | ai.txt |

Click **Send**.

Example response:

```json
{
    "status": "success",
    "documents_uploaded": 1,
    "chunks_created": 6
}
```

---

## 3. Test the Prompt Endpoint

Create a request:

**Method**

```
POST
```

**URL**

```
http://127.0.0.1:8000/prompt
```

Go to:

```
Body → raw → JSON
```

Example request:

```json
{
    "query": "What is FastAPI?"
}
```

Example response:

```json
{
    "answer": "...",
    "context_used": [
        "..."
    ]
}
```

---

## 4. Test Retrieval

Upload a document containing unique information, for example:

```
The capital of Wakanda is Birnin Zana.
```

Then send:

```json
{
    "query": "What is the capital of Wakanda?"
}
```

Expected response:

```json
{
    "answer": "The capital of Wakanda is Birnin Zana.",
    "context_used": [
        "The capital of Wakanda is Birnin Zana."
    ]
}
```

This verifies that the answer is generated from the uploaded document rather than the model's general knowledge.

---

# Environment Variables

| Variable | Description |
|----------|-------------|
| HF_API_KEY | HuggingFace API key |
| EMBED_MODEL_NAME | Sentence Transformer embedding model |
| GEMINI_API_KEY | Gemini API key |
| LLM_MODEL_NAME | Gemini model name |
| CHROMA_DB_HOST | ChromaDB server host |
| CHROMA_DB_PORT | ChromaDB server port |
| RAG_DATA_DIR | Directory for uploaded/indexed data |
| CHUNK_LENGTH | Chunk size used during semantic chunking |
| SERVER_PORT | FastAPI server port |
